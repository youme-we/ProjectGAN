ProjectGAN:
	@docker compose up -d && docker attach projectgan-NN-1

run: 
	@cd NN && python3 wrapper.py

plot:
	@cd UI && cd server && npx nodemon server.js 

development:
	@cd UI && cd client && npm start 

compille:
	@cd NN && cd datamanagement && python3 compille_data.py

