import React, { Component } from "react";

class Network extends Component {
  Neuronal_Net = () => {
    let markcolor = ["#628E25", "#6286AD"];
    const style = {
      //stroke: '#628E25', //#628E25,#6286AD '
      position: "relative",
      Zindex: 10,
    };
    const lyers_shape_neurons = {
      size_net: 600,
      top: 1200,
      stroke_with: 2,
      scale_x: 350,
      radius_neurons: 15,
      left: 100,
    };
    //var stroke_with = lyers_shape_neurons.stroke_with;
    //var strong_lyers_shape = lyers_shape_neurons.strong_lyers_shape
    const left = lyers_shape_neurons.left;
    const radius_neurons = lyers_shape_neurons.radius_neurons;
    const scale_x = lyers_shape_neurons.scale_x;
    const top = lyers_shape_neurons.top;
    const size_net = lyers_shape_neurons.size_net;
    //var lyers_shape = lyers_shape_neurons.lyers_shape

    const lyers_shape = [1, 2]; //shape of NN
    //Array.from(lyers_shape.toString()).map(Number);

    var strong_lyers_shape = this.props.weights; //weights of NN;

    var second_lyer_a = []; //nimmt jeden zwieten Wert von lyers_shape :jede ungerade Stelle der Array
    for (var i = 0; i < lyers_shape.length; i = i + 2) {
      second_lyer_a.push(lyers_shape[i + 1]);
    }

    var first_lyer_a = []; //nimmt jeden zweiten Wert von lyers_shape:jede gerade Stelle der Array
    for (i = 0; i < lyers_shape.length; i = i + 2) {
      first_lyer_a.push(lyers_shape[i]);
    }

    var x_values_a = first_lyer_a.map(
      (
        x_p,
        x //hier werden die x Kordienaten berechnet
      ) => {
        return x * scale_x + scale_x; //1,2,3,4,5...solang bis die hälfte der länge von den Werten der neuronen Erreicht ist also bis die länge von den 2D Arrays firrst_lyer_a oder second_lyer_a erreicht ist * 250 +250+100(da es nicht an dem linken Rand beginnen soll)
      }
    );

    second_lyer_a = second_lyer_a.map(
      (
        data_p,
        data //generiert aus den Daten eine 2D Array
      ) =>
        Array(second_lyer_a[data] - 1 + 1)
          .fill()
          .map((_, idx) => 1 + idx) //generiert Array von 1-second_lyer_a[data]
    );

    first_lyer_a = first_lyer_a.map(
      (
        data_p,
        data //generiert aus den Daten eine 2D Array
      ) =>
        Array(first_lyer_a[data] - 1 + 1)
          .fill()
          .map((_, idx) => 1 + idx) //generiert Array von 1-first_lyer_a[data]
    );

    i = 0;

    const line_values = new Array(first_lyer_a, second_lyer_a); //daten für die neuronenanzahl werden werden aus zwei 2D Arrays zu einer 3D Array zuammengeführt
    var x_of_resize_dot = 0;
    var y_of_resize_dot = 0;
    return (
      <div className="basis-2/3">
        <svg>
          {x_values_a.map((x_values_p, x_values) =>
            line_values[0][x_values].map((first_lyer_p, first_lyer) =>
              line_values[1][x_values].map((second_lyer_p, second_lyer) => {
                if (Math.sign(strong_lyers_shape[i]) === 1) {
                  //Wenn stronge_lyers_shape(die Gewichte) poitiv sind, ist stroke_color grün und wenn es negativ ist es rot
                  var stroke_color = markcolor[0];
                } else {
                  stroke_color = markcolor[1];
                }
                x_of_resize_dot = x_values_p + left - scale_x;
                y_of_resize_dot =
                  first_lyer_p *
                  (size_net / (line_values[0][x_values].length + 1)) +
                  top;
                return (
                  <g key={i}>
                    <rect
                      width="90"
                      height="90"
                      fill=""
                      fillOpacity="0"
                      x={x_values_p + left - scale_x - 50}
                      y={
                        first_lyer_p *
                        (size_net / (line_values[0][x_values].length + 1)) +
                        top -
                        50
                      }
                    />
                    <rect
                      width="40"
                      height="40"
                      fill=""
                      fillOpacity="0"
                      x={x_values_p + left}
                      y={
                        second_lyer_p *
                        (size_net / (line_values[1][x_values].length + 1)) +
                        top -
                        50
                      }
                    />
                    <line
                      style={style}
                      x1={
                        x_values_p -
                        scale_x +
                        radius_neurons +
                        left /* 800-700+10+100*/
                      }
                      x2={x_values_p - radius_neurons + left}
                      y1={
                        first_lyer_p *
                        (size_net / (line_values[0][x_values].length + 1)) +
                        top
                      }
                      y2={
                        second_lyer_p *
                        (size_net / (line_values[1][x_values].length + 1)) +
                        top
                      }
                      strokeWidth={
                        Math.abs(strong_lyers_shape[i]) +
                        0.6 /*Es werden alle Werte positiv gemacht und noch 0.6 addiert, falls ein Gewicht < 0.5 ist, da mann sonst nicht die Line erkennen kann*/
                      }
                      stroke={stroke_color}
                    >
                      {" "}
                    </line>
                    ,
                    <circle
                      cx={x_values_p + left}
                      cy={
                        second_lyer_p *
                        (size_net / (line_values[1][x_values].length + 1)) +
                        top
                      }
                      r={radius_neurons}
                      stroke="black"
                      strokeWidth="3"
                      fill="white"
                    />
                    ,
                    <circle
                      cx={x_values_p + left - scale_x}
                      cy={
                        first_lyer_p *
                        (size_net / (line_values[0][x_values].length + 1)) +
                        top
                      }
                      r={radius_neurons}
                      stroke="black"
                      strokeWidth="3"
                      fill="white"
                    />
                    ,{(i = i + 1)}
                  </g>
                );
              })
            )
          )}
        </svg>
      </div>
    );
  };

  render() {
    return <this.Neuronal_Net />;
  }
}

export default Network;
