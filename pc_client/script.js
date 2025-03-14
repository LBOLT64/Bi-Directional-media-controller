// Get references to status and response elements
const statusEl = document.getElementById("status");
const responseEl = document.getElementById("response");

// Create a new WebSocket connection. Replace with your PC's IP.
const ws = new WebSocket("ws://your_ip:8765");

ws.onopen = () => {
  console.log("Connected to WebSocket server");
  statusEl.textContent = "Connected";
  statusEl.style.background = "#d4edda";
  // Send an initialization message identifying this client as "android"
  ws.send(JSON.stringify({ init: true, device: "pc" }));
};

ws.onerror = (error) => {
  console.error("WebSocket Error:", error);
  statusEl.textContent = "Error connecting";
  statusEl.style.background = "#f8d7da";
};

ws.onclose = () => {
  console.log("WebSocket connection closed");
  statusEl.textContent = "Disconnected";
  statusEl.style.background = "#f8d7da";
};

ws.onmessage = (event) => {
  console.log("Server Response:", event.data);
  responseEl.textContent = event.data;
};

// Function to send a command to the server.
function sendCommand(command) {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ action: command }));
    console.log("Sent command:", command);
  } else {
    console.error("WebSocket is not connected.");
  }
}
