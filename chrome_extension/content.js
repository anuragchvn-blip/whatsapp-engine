(async function() {
  // Wait for WhatsApp Web UI to load
  await new Promise(r => setTimeout(r, 5000));

  // Retrieve message from storage
  chrome.storage.local.get("message", ({ message }) => {
    if (!message) return;

    // Find message box and send button
    const messageBox = document.querySelector("div[contenteditable='true'][data-tab='10']");
    if (messageBox) {
      // Paste message
      messageBox.textContent = message;

      // Trigger input event
      messageBox.dispatchEvent(new InputEvent("input", { bubbles: true }));

      // Click send
      const sendBtn = document.querySelector("span[data-icon='send']");
      if (sendBtn) {
        setTimeout(() => sendBtn.click(), 500);
      }
    }
  });
})();
// This code is for the content.js file of a Chrome extension that sends WhatsApp messages