// script.js for Android Client
const statusEl = document.getElementById("status");
const responseEl = document.getElementById("response");

// Replace the IP address with your PC's IP.
const ws = new WebSocket("ws://192.168.73.82:8765");

ws.onopen = () => {
  console.log("Connected to WebSocket server");
  statusEl.textContent = "Connected";
  statusEl.style.background = "#d4edda";
  // Send an initialization message identifying this client as "android"
  ws.send(JSON.stringify({ init: true, device: "android" }));
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

function sendCommand(command) {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ action: command }));
    console.log("Sent command:", command);
  } else {
    console.error("WebSocket is not connected.");
  }
}
