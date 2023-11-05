run: 
	cd NN && python3 wrapper.py

plot:
	cd UI && cd server && npx nodemon server.js 

compress:
	cd NN && cd datamanagement && python3 compress_data.py

