const icons = {laptop:"💻",phone:"📱",headphones:"🎧",smartwatch:"⌚",tablet:"📱"};

function usePrompt(text){
  document.getElementById("query").value = text;
  recommend();
}

async function recommend(){
  const query = document.getElementById("query").value.trim();
  const status = document.getElementById("status");
  const results = document.getElementById("results");

  if(!query){
    status.textContent = "Please describe what you want to buy.";
    return;
  }

  status.textContent = "🤖 Agent is analyzing your intent and ranking products...";
  results.innerHTML = "";

  try{
    const response = await fetch("/api/recommend", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({query})
    });
    const data = await response.json();

    if(!response.ok) throw new Error(data.error || "Request failed");

    status.textContent = "✓ Recommendation complete";

    results.innerHTML = `
      <div class="summary">
        <strong>Agent reasoning:</strong> ${data.summary}
        <br><br>
        <strong>Detected preferences:</strong>
        ${data.intent.preferences.length ? data.intent.preferences.join(", ") : "general shopping"}
      </div>
      ${data.recommendations.map((p,i)=>`
        <article class="card">
          <div class="icon">${icons[p.category] || "🛍️"}</div>
          <h3>${i+1}. ${p.name}</h3>
          <div class="price">₹${p.price.toLocaleString("en-IN")}</div>
          <div class="rating">★ ${p.rating}</div>
          <p>${p.description}</p>
          ${p.reasons.map(r=>`<div class="reason">✓ ${r}</div>`).join("")}
        </article>
      `).join("")}
    `;
  }catch(err){
    status.textContent = "Error: " + err.message;
  }
}
