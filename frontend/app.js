document.getElementById('check').onclick = async function(){
  const city = document.getElementById('city').value || 'Delhi';
  const age = document.getElementById('age').value || 25;
  const asthma = document.getElementById('asthma').checked ? 1 : 0;
  const smoker = document.getElementById('smoker').checked ? 1 : 0;
  const url = `http://127.0.0.1:5000/current?city=${encodeURIComponent(city)}&age=${age}&asthma=${asthma}&smoker=${smoker}`;
  try {
    const r = await fetch(url);
    const data = await r.json();
    document.getElementById('result').style.display='block';
    document.getElementById('result').innerHTML = `
      <div class="aqi">AQI: ${data.aqi} (${data.aqi_category})</div>
      <div><strong>Risk:</strong> ${data.risk}</div>
      <div><strong>PM2.5:</strong> ${data.pm2_5 || 'N/A'} | <strong>PM10:</strong> ${data.pm10 || 'N/A'}</div>
      <h4>Recommendations</h4>
      <ul>${data.recommendations.map(x => `<li>${x}</li>`).join('')}</ul>
    `;
  } catch (e) {
    alert("Failed to fetch API. Make sure backend is running (python backend/app.py). Error: "+e);
  }
};