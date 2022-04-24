curl -H "Accept: application/json" -H "Content-type: application/json" \
-X POST -d '{"categories":["Recommended", "Newly Added"], "genres":["Suspense", "Crime"], "platforms":["Disney HotStar", "Netflix"], "awards":["Oscars"], "ebitsRatingRange": [5,7]}' \
http://localhost:8000/api/v1/movies/
