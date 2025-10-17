// Copy to clipboard functionality for code blocks
document.addEventListener('DOMContentLoaded', function() {
  // Find all code blocks
  const codeBlocks = document.querySelectorAll('pre code, .highlight pre, .highlighter-rouge pre');
  
  codeBlocks.forEach(function(codeBlock) {
    // Skip if already processed
    if (codeBlock.parentNode.querySelector('.copy-btn')) {
      return;
    }
    
    // Create copy button
    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-btn';
    copyBtn.textContent = 'Copy';
    copyBtn.setAttribute('aria-label', 'Copy code to clipboard');
    
    // Add click event listener
    copyBtn.addEventListener('click', function(e) {
      // Prevent event bubbling
      e.stopPropagation();
      
      // Get the code text, excluding the button
      let codeText = '';
      
      // Clone the code block to avoid affecting the original
      const tempCodeBlock = codeBlock.cloneNode(true);
      
      // Remove any copy buttons from the cloned element
      const copyButtons = tempCodeBlock.querySelectorAll('.copy-btn');
      copyButtons.forEach(btn => btn.remove());
      
      // Get the cleaned text content
      codeText = tempCodeBlock.textContent || tempCodeBlock.innerText;
      
      // Clean up the text (remove extra whitespace, etc.)
      codeText = codeText.trim();
      
      // Copy to clipboard
      navigator.clipboard.writeText(codeText).then(function() {
        // Show success feedback
        copyBtn.textContent = '';
        copyBtn.classList.add('copied');
        
        // Reset button after 2 seconds
        setTimeout(function() {
          copyBtn.textContent = 'Copy';
          copyBtn.classList.remove('copied');
        }, 2000);
      }).catch(function(err) {
        // Fallback for older browsers
        console.error('Failed to copy text: ', err);
        fallbackCopyTextToClipboard(codeText, copyBtn);
      });
    });
    
    // Add button to the code block container
    const container = codeBlock.parentNode;
    
    // Make sure the container has relative positioning
    if (container.tagName === 'PRE') {
      container.style.position = 'relative';
      container.appendChild(copyBtn);
    } else if (container.classList.contains('highlight')) {
      container.appendChild(copyBtn);
    } else {
      // Wrap in a relative positioned div if needed
      const wrapper = document.createElement('div');
      wrapper.style.position = 'relative';
      wrapper.style.display = 'inline-block';
      wrapper.style.width = '100%';
      
      container.insertBefore(wrapper, codeBlock);
      wrapper.appendChild(codeBlock);
      wrapper.appendChild(copyBtn);
    }
  });
});

// Fallback function for browsers that don't support navigator.clipboard
function fallbackCopyTextToClipboard(text, button) {
  const textArea = document.createElement('textarea');
  textArea.value = text;
  
  // Avoid scrolling to bottom
  textArea.style.top = '0';
  textArea.style.left = '0';
  textArea.style.position = 'fixed';
  textArea.style.opacity = '0';
  
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  
  try {
    const successful = document.execCommand('copy');
    if (successful) {
      button.textContent = '';
      button.classList.add('copied');
      
      setTimeout(function() {
        button.textContent = 'Copy';
        button.classList.remove('copied');
      }, 2000);
    } else {
      button.textContent = 'Failed';
      setTimeout(function() {
        button.textContent = 'Copy';
      }, 2000);
    }
  } catch (err) {
    console.error('Fallback: Oops, unable to copy', err);
    button.textContent = 'Failed';
    setTimeout(function() {
      button.textContent = 'Copy';
    }, 2000);
  }
  
  document.body.removeChild(textArea);
}
