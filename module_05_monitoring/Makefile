

make run: 
	uv run python assistant.py

chat: 
	uv run streamlit run app.py

network:
	docker network create monitoring

postgres: network
	docker run -it \
		--name course-assistant-pg \
		--network monitoring \
		-e POSTGRES_USER=user \
		-e POSTGRES_PASSWORD=password \
		-e POSTGRES_DB=course_assistant \
		-p 5433:5432 \
		-v pgdata_v2:/var/lib/postgresql/data \
		postgres:17