var ec_eg = echarts.init(document.getElementById("engagement"));

var option_eg = {
  title: {
    text: 'Engagement Trend'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['Comment', 'Ups', 'Downs']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  toolbox: {
    feature: {
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: 'Comment',
      type: 'line',
      stack: 'Total',
      data: []
    },
    {
      name: 'Ups',
      type: 'line',
      stack: 'Total',
      data: []
    },
    {
      name: 'Downs',
      type: 'line',
      stack: 'Total',
      data: []
    }
  ]
};

ec_eg.setOption(option_eg);

