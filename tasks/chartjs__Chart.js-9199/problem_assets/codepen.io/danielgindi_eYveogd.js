var config = {
  "type": "bar",
  "options": {
    "responsive": true,
    "plugins": {
      "legend": {
        "position": "top",
        "rtl": true,
        textDirection: 'rtl'
      }
    },
  },
  "data": {
    "datasets": [
      {
        "data": [
          123.4567,
        ],
        "label": 'בדיקה עם rtl?'
      }
    ],
    "labels": [
      "בדיקה",
    ]
  }
};

new Chart('chart', config);