run: 
	cd NN && python3 wrapper.py #NN

plot:
	cd UI && cd server && npx nodemon server.js #starts server

development:
	cd UI && cd client && npm start #starts client

compress:
	cd NN && cd datamanagement && python3 compress_data.py

