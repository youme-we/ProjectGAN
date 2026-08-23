ProjectGAN:
	@docker compose up -d && docker attach projectgan-nn-1

ProjectGAN_server:
	@docker compose -f docker-compose_server.yaml up -d


run: 
	@cd NN && python3 wrapper.py

plot:
	@cd UI && cd server && npx nodemon main.js 

devl:
	@cd UI && cd client && npm run dev 

compille:
	@cd HOST && uv run python compille_data.py

