// sample payloads
const SAMPLES = {
  spam: {
    subject: "Win a FREE iPhone now!",
    body: `Congratulations! You have been selected to win a brand new iPhone. 
Click the link below to claim your prize before it expires: 
http://fake-prize-link.com`
  },
tricky: {
  subject: "Reminder: Company lunch tomorrow",
  body: `Hello team,

Don't forget the company lunch tomorrow at 12:30pm in the cafeteria.
Please RSVP to confirm attendance.`
},
  ham: {
    subject: "Lunch plans?",
    body: `Hey,
Are we still on for lunch tomorrow at noon? Let me know.`
  }
};


function setStatus(message, kind = "neutral") {
  const statusBox = document.getElementById("statusBox");
  statusBox.className = "rounded-lg p-3";
  if (kind === "spam") {
    statusBox.classList.add(
      "bg-rose-50",
      "border",
      "border-rose-100",
      "text-rose-800"
    );
  } else if (kind === "ham") {
    statusBox.classList.add(
      "bg-emerald-50",
      "border",
      "border-emerald-100",
      "text-emerald-800"
    );
  } else if (kind === "error") {
    statusBox.classList.add(
      "bg-amber-50",
      "border",
      "border-amber-100",
      "text-amber-800"
    );
  } else {
    statusBox.classList.add(
      "bg-slate-50",
      "border",
      "border-slate-100",
      "text-slate-600"
    );
  }
  statusBox.innerHTML = message;
}

document.querySelectorAll(".load-sample").forEach((btn) => {
  btn.addEventListener("click", () => {
    const sample = btn.dataset.sample;
    document.getElementById("subject").value = SAMPLES[sample].subject;
    document.getElementById("body").value = SAMPLES[sample].body;
  });
});

document.getElementById("check").addEventListener("click", async () => {
  const subject = document.getElementById("subject").value.trim();
  const body = document.getElementById("body").value.trim();

  if (!body) {
    alert("Please paste email text into the body field.");
    return;
  }

  setStatus("Checking — sending request...", "neutral");
  document.getElementById("probWrapper").classList.add("hidden");
  document.getElementById("explain").classList.add("hidden");

  try {
    const resp = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: body, subject: subject }),
    });

    const text = await resp.text();
    let data;
    try {
      data = JSON.parse(text);
    } catch (err) {
      throw new Error("Non-JSON response: " + (text || "[empty]"));
    }

    if (!resp.ok) {
      setStatus("Server error: " + JSON.stringify(data), "error");
      return;
    }

    const pred = data.prediction === 1 ? "SPAM" : "NOT SPAM";
    const spamProb =
      data.spam_probability !== null && data.spam_probability !== undefined
        ? Number(data.spam_probability)
        : null;

    if (spamProb === null || Number.isNaN(spamProb)) {
      setStatus(
        `<strong>Prediction:</strong> ${pred} — confidence unavailable`,
        data.prediction === 1 ? "spam" : "ham"
      );
      document.getElementById("probWrapper").classList.add("hidden");
      return;
    }

    const percent = Math.round(spamProb * 100);
    document.getElementById("probText").innerText = percent + "%";
    document.getElementById("probBar").style.width = percent + "%";

    if (percent >= 70) {
      document.getElementById("probBar").style.background =
        "linear-gradient(90deg,#ff5c5c,#ff8b5c)";
    } else if (percent >= 35) {
      document.getElementById("probBar").style.background =
        "linear-gradient(90deg,#ffd166,#ff8b5c)";
    } else {
      document.getElementById("probBar").style.background =
        "linear-gradient(90deg,#8ef6b9,#50c878)";
    }

    document.getElementById("probWrapper").classList.remove("hidden");
    setStatus(
      `<strong>Prediction:</strong> ${pred}`,
      data.prediction === 1 ? "spam" : "ham"
    );
    document.getElementById("explain").classList.remove("hidden");
  } catch (err) {
    setStatus("Request failed: " + err.message, "error");
  }
});
