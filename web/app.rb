require 'sinatra'
require 'mongo'
require_relative './litter_service'

set :bind, '0.0.0.0'
set :port, 4567

service = LitterService.new

post '/litter_usage' do
  data = JSON.parse(request.body.read)
  id = service.store_litter_usage(data)
  return { id: id.to_s }.to_json
end

post '/usage_video' do
  data = JSON.parse(request.body.read)
  id = service.store_usage_video(data)
  return { id: id.to_s }.to_json
end

post '/query_usage' do
  query = JSON.parse(request.body.read)
  result = service.query_litter_usage(query)
  return result.to_json
end

post '/usage_videos' do
  ids = JSON.parse(request.body.read)
  result = service.get_usage_videos(ids)
  return result.to_json
end

get '/' do
  @usages_by_cat = service.count_usages_last_24_hours_by_cat
  return erb :dashboard
end
