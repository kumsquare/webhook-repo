const EVENTS_API = "http://127.00.1:5000/webhook/events";
const list = document.getElementById("events");

function formatEvent(event) {
  const date = new Date(event.timestamp).toUTCString();

  if (event.action === "PUSH") {
    return `${event.author} pushed to "${event.to_branch}" on ${date}`;
  }

  if (event.action === "PULL_REQUEST") {
    return `${event.author} submitted a pull request from "${event.from_branch}" to "${event.to_branch}" on ${date}`;
  }

  if (event.action === "MERGE") {
    return `${event.author} merged branch "${event.from_branch}" to "${event.to_branch}" on ${date}`;
  }

  return "";
}

async function fetchEvents() {
  try {
    const res = await fetch(EVENTS_API);
    const data = await res.json();

    data.sort((a,b) => new Date(b.timestamp) - new Date(a.timestamp));

    list.innerHTML = "";

    data.forEach(event => {
      const li = document.createElement("li");
      li.textContent = formatEvent(event);
      list.appendChild(li);
    });
  } catch (err) {
    console.error("Failed to fetch events", err);
  }
}

// initial load
fetchEvents();

// poll every 15 seconds
setInterval(fetchEvents, 15000);
