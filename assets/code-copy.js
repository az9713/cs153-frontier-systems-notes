document.querySelectorAll('pre > code').forEach((code) => {
  const button = document.createElement('button');
  button.textContent = 'Copy code';
  button.type = 'button';
  button.className = 'copy-code';
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(code.textContent);
      button.textContent = 'Copied';
    } catch {
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      button.textContent = 'Selected: press Ctrl+C';
    }
  });
  code.parentElement.before(button);
});
