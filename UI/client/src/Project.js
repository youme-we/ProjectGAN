import React, { useEffect, useState } from 'react'
import { useNavigate } from "react-router-dom"
import * as echarts from 'echarts';



function Project() {
  const [backendData, setBackendData] = useState([{}])
  const [UsrInputValue, setUsrInputValue] = useState("")
  const [PassInputValue, setPassInputValue] = useState("")
  const navigate = useNavigate();

  // Create the echarts instance
  var myChart = echarts.init(document.getElementById('main'));

  // Draw the chart
  myChart.setOption({
    title: {
      text: 'ECharts Getting Started Example'
    },
    tooltip: {},
    xAxis: {
      data: ['shirt', 'cardigan', 'chiffon', 'pants', 'heels', 'socks']
    },
    yAxis: {},
    series: [
      {
        name: 'sales',
        type: 'bar',
        data: [5, 20, 36, 10, 10, 20]
      }
    ]
  });

  const Send = () => {
    fetch('http://localhost:3001/project', {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ usr: UsrInputValue, pass: PassInputValue })
    })
      .then(response => response.json())
      .then(res => {
        if (res) {
          navigate('/auth')
        }
      })
  }



  return (
    <div className="Project">
      <h1>Project</h1>
      <div className='main'></div>
    </div>
  );
}

export default Project;


