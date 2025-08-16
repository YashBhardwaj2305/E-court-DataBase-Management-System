// document.querySelector("form").addEventListener("submit", function (event) {
//   event.preventDefault();
//   let caseNumber = document.querySelector("#case-number").value;
//   if (caseNumber) {
//     alert(`Searching for case number: ${caseNumber}`);
//   } else {
//     alert("Please enter a case number.");
//   }
// });


// Select all navigation links within the MainMenu
const navLinks = document.querySelectorAll('.MainMenu .nav-link');

// Loop through each link and add a click event listener
navLinks.forEach(link => {
    link.addEventListener('click', function(event) {
        // Prevent the default action of the link (optional)
        // event.preventDefault();
        
        // Remove the 'active' class from all links
        navLinks.forEach(nav => nav.classList.remove('active'));
        
        // Add the 'active' class to the clicked link
        this.classList.add('active');
    });
});

function addField(type) {
    const container = document.getElementById(`${type}-container`);
    const input = document.createElement('input');
    input.type = "text";
    input.name = `${type}[]`;
    input.placeholder = `Enter ${type.charAt(0).toUpperCase() + type.slice(1)}`;

    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.classList.add('delete-btn');
    deleteButton.textContent = '×';
    deleteButton.onclick = function () {
        container.removeChild(input);
        container.removeChild(deleteButton);
    };

    container.appendChild(input);
    container.appendChild(deleteButton);
}

function resetSection(sectionId) {
  const section = document.getElementById(sectionId);
  const inputs = section.querySelectorAll('input, select');
  inputs.forEach(input => {
      if (input.type === "text" || input.type === "number" || input.type === "date" || input.type === "time") {
          input.value = "";
      } else if (input.tagName === "SELECT") {
          input.selectedIndex = 0; // Reset to first option
      }
  });
}

function addField(containerId) {
  const container = document.getElementById(containerId + '-container');
  const input = document.createElement("input");
  input.type = "text";
  input.name = containerId + "[]";
  input.placeholder = `Enter ${containerId.slice(0, -1).toUpperCase()} Name`;
  container.appendChild(input);

  const button = document.createElement("button");
  button.type = "button";
  button.classList.add("add-field");
  button.textContent = "+";
  button.onclick = function() {
      addField(containerId);
  };
  container.appendChild(button);
}

var marquee = document.getElementById("myMarquee");
  marquee.onmousedown = function() {
    this.stop();
  };
  marquee.onmouseup = function() {
    this.start();
  };

  function toggleContent(element) {
    const section = element.parentElement;
    section.classList.toggle("active");
}

function showLoginForm(userType) {
  const formContainer = document.getElementById('login-form-container');
  let signUpHTML = '';

  if (userType === 'User') {
      signUpHTML = `
          <div class="form-footer">
              <p>Don't have an account? <a href="/signup">Sign Up</a></p>
          </div>
      `;
  }

  formContainer.innerHTML = `
      <form action="{{ url_for('login') }}" method="POST">
      <h1>${userType} Login</h1>    
      <div class="form-group">
              <label for="email">${userType} Email</label>
              <input type="text" id="email" name="email" required>
          </div>
          <div class="form-group">
              <label for="password">${userType} Password</label>
              <input type="password" id="password" name="password" required>
          </div>
          <input type="hidden" name="userType" value="${userType}">
          <button type="submit" class="login-btn">Login as ${userType}</button>
      </form>
      ${signUpHTML}
  `;
}