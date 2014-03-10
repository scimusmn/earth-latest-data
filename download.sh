cd data/
rm -rf *
curl "http://www.nacis.org/naturalearth/50m/physical/ne_50m_coastline.zip" -o ne_50m_coastline.zip
curl "http://www.nacis.org/naturalearth/50m/physical/ne_50m_lakes.zip" -o ne_50m_lakes.zip
curl "http://www.nacis.org/naturalearth/110m/physical/ne_110m_coastline.zip" -o ne_110m_coastline.zip
curl "http://www.nacis.org/naturalearth/110m/physical/ne_110m_lakes.zip" -o ne_110m_lakes.zip
curl "http://www.nacis.org/naturalearth/110m/cultural/ne_110m_admin_1_states_provinces_lines.zip" -o ne_110m_admin_1_states_provinces_lines.zip
curl "http://www.nacis.org/naturalearth/110m/cultural/ne_110m_admin_0_boundary_lines_land.zip" -o ne_110m_admin_0_boundary_lines_land.zip

unzip -o ne_\*.zip
ogr2ogr -f GeoJSON coastline_50m.json ne_50m_coastline.shp
ogr2ogr -f GeoJSON coastline_110m.json ne_110m_coastline.shp
ogr2ogr -f GeoJSON -where "scalerank < 4" lakes_50m.json ne_50m_lakes.shp
ogr2ogr -f GeoJSON -where "scalerank < 2 AND admin='admin-0'" lakes_110m.json ne_110m_lakes.shp
ogr2ogr -f GeoJSON -simplify 1 coastline_tiny.json ne_110m_coastline.shp
ogr2ogr -f GeoJSON -simplify 1 -where "scalerank < 2 AND admin='admin-0'" lakes_tiny.json ne_110m_lakes.shp
ogr2ogr -f GeoJSON states_provinces_lines.json ne_110m_admin_1_states_provinces_lines.shp
ogr2ogr -f GeoJSON admin_0_boundary_lines_land.json ne_110m_admin_0_boundary_lines_land.shp

topojson -o earth-topo.json \
  admin_0_boundary_lines_land.json states_provinces_lines.json \
  coastline_50m.json coastline_110m.json lakes_50m.json lakes_110m.json
topojson -o earth-topo-mobile.json\
  admin_0_boundary_lines_land.json states_provinces_lines.json \
  coastline_110m.json coastline_tiny.json lakes_110m.json lakes_tiny.json
cp earth-topo*.json ~/src/wind/public/data/
