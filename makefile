ProjectGAN:
	@docker compose up -d && docker attach projectgan-nn-1

ProjectGAN_server:
	@docker compose -f docker-compose_server.yaml up -d


run: 
	@cd NN && python3 wrapper.py

plot:
	@cd UI && cd server && npx nodemon server.js 

development:
	@cd UI && cd client && npm start 

compille:
	@cd HOST && python3 compille_data.py

