
  <div className="relative top-0 right-0 w-screen h-screen bg-white-brown">
    <Controllers_pps socket={socket} />
      {metrics.epoch &&
          <div className="flex h-full justify-evenly relative top-48 bg-dark-green">
            <Chart_EL metrics={metrics} />
            <Inputfields_Hyperparameters overview={overview} setoverview={setoverview} overview_template={overview_template} socket={socket} />
          </div>
              }
          <div className="flex justify-evenly relative top-16 bg-dark-green">
            <Samples_TT metrics={metrics} />
          </div>
          <Network weights={metrics.weights} />
        }

    </div>
