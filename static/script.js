document.addEventListener('DOMContentLoaded', () => {
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('nav-links');

  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('show');
  });

  // NEW: Handle form submission for summarizing
  const form = document.querySelector('form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent default form redirect

    const loader = document.getElementById("loader");
    loader.style.display = "flex";

    const summaryDiv = document.getElementById("summary-result");
    summaryDiv.innerHTML = ''; // Clear previous summary

    const formData = new FormData(form);

    try {
      const response = await fetch('/summarize', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      loader.style.display = "none";

      if (response.ok) {
        summaryDiv.innerHTML = `
          <h3>📄 Summary:</h3>
          <pre style="white-space: pre-wrap; background: #f9f9f9; padding: 10px; border-radius: 10px;">${data.summary}</pre>
        `;
      } else {
        summaryDiv.innerHTML = `<p style="color:red;">${data.error || 'Something went wrong.'}</p>`;
      }
    } catch (err) {
      loader.style.display = "none";
      summaryDiv.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
    }
  });
});
