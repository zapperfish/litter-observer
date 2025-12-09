require 'mongo'

DEFAULT_CAT_WEIGHTS_KG = {
  "Feather" => 6.0,
  "Frances" => 4.0
}


class LitterService
  def initialize
    client = Mongo::Client.new(['127.0.0.1:27017'], database: 'litter_db')
    @usage = client[:litter_usage]
    @videos = client[:usage_videos]

    # Create unique index on cat_name + timestamp
    @usage.indexes.create_one(
      { "cat_metadata.cat_name" => 1, "usage_timestamp_unix_ns" => 1 },
      unique: true
    )

    @mutex = Mutex.new
    @cat_name_to_weight_kg = _load_last_cat_weights()
  end

  def _load_last_cat_weights()
    cat_name_to_weight_kg = {}
    DEFAULT_CAT_WEIGHTS_KG.each do |cat_name, default_weight_kg|
      last_doc = @usage.find({"cat_metadata.cat_name" => cat_name}).sort({"usage_timestamp_unix_ns" => -1}).limit(1).first
      if last_doc
        cat_name_to_weight_kg[cat_name] = last_doc["cat_metadata"]["cat_weight_kg"]
      else
        cat_name_to_weight_kg[cat_name] = default_weight_kg
      end
    end

    return cat_name_to_weight_kg
  end

  def _determine_likely_cat_and_update_weight(recorded_weight_kg)
    likely_cat_name = "unknown"
    @mutex.synchronize do
      closest_weight_kg = -1
      @cat_name_to_weight_kg.each do |cat_name, weight_kg|
        if (weight_kg - recorded_weight_kg).abs < (closest_weight_kg - recorded_weight_kg).abs
          closest_weight_kg = weight_kg
          likely_cat_name = cat_name
        end
      end
      @cat_name_to_weight_kg[likely_cat_name] = recorded_weight_kg
    end

    return likely_cat_name
  end

  def store_litter_usage(data)
    recorded_weight_kg = data["cat_metadata"]["cat_weight_kg"]
    if recorded_weight_kg != -1
      data["cat_metadata"]["cat_name"] = _determine_likely_cat_and_update_weight(recorded_weight_kg)
    end

    res = @usage.find_one_and_update(data, {"$setOnInsert" => data}, upsert: true, return_document: :after)
    return res["_id"].to_s
  end

  def store_usage_video(data)
    res = @videos.insert_one(data)
    return res.inserted_id
  end

  def query_litter_usage(query)
    return @usage.find(query).to_a
  end

  def get_usage_videos(ids)
    bson_ids = ids.map { |i| BSON::ObjectId.from_string(i) }
    return @videos.find({ litter_usage_id: { "$in": bson_ids } }).to_a
  end

  def count_usages_last_24_hours_by_cat
    twenty_four_hours_ago_ns = (Time.now.to_i - 86400) * 1_000_000_000
    
    pipeline = [
      { "$match" => { "usage_timestamp_unix_ns" => { "$gte" => twenty_four_hours_ago_ns } } },
      { "$group" => { "_id" => "$cat_metadata.cat_name", "count" => { "$sum" => 1 } } }
    ]
    
    results = @usage.aggregate(pipeline).to_a || []
    return results.map { |r| [r["_id"], r["count"]] }.to_h
  end
end
