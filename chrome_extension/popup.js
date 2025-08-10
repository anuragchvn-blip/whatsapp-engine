document.getElementById('sendBtn').addEventListener('click', async function() {
  const message = document.getElementById('message').value.trim();
  const phones = document.getElementById('phones').value.trim();
  const statusDiv = document.getElementById('status');

  if (!message || !phones) {
    statusDiv.textContent = 'Please enter both message and phone numbers.';
    return;
  }

  const phoneList = phones.split(',').map(p => p.trim()).filter(Boolean);
  statusDiv.textContent = `Sending to ${phoneList.length} numbers...`;

  chrome.storage.local.set({ message });

  for (let i = 0; i < phoneList.length; i++) {
    const phone = phoneList[i].replace(/[^\d+]/g, '');
    const url = `https://web.whatsapp.com/send?phone=${encodeURIComponent(phone)}&text=${encodeURIComponent(message)}`;
    chrome.tabs.create({ url });
    await new Promise(r => setTimeout(r, 6000 + Math.random() * 2000)); // Delay between opens
  }

  statusDiv.textContent = 'All messages sent automatically!';
});
