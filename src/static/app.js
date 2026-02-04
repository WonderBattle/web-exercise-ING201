document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to attach event listeners to remove buttons
  function attachRemoveListeners(activityCard) {
    const removeButtons = activityCard.querySelectorAll('.remove-btn');
    removeButtons.forEach(button => {
      button.addEventListener('click', async (event) => {
        const email = event.target.dataset.email;
        const activity = event.target.dataset.activity;

        try {
          const response = await fetch(
            `/activities/${encodeURIComponent(activity)}/remove?email=${encodeURIComponent(email)}`,
            {
              method: "DELETE",
            }
          );

          const result = await response.json();

          if (response.ok) {
            messageDiv.textContent = result.message;
            messageDiv.className = "success";

            // Update the activity card
            const updatedDetails = {
              ...JSON.parse(activityCard.dataset.activityDetails),
              participants: JSON.parse(activityCard.dataset.activityDetails).participants.filter(p => p !== email)
            };
            updateActivityCard(activityCard, updatedDetails);
            activityCard.dataset.activityDetails = JSON.stringify(updatedDetails);
          } else {
            messageDiv.textContent = result.detail || "An error occurred";
            messageDiv.className = "error";
          }

          messageDiv.classList.remove("hidden");

          // Hide message after 5 seconds
          setTimeout(() => {
            messageDiv.classList.add("hidden");
          }, 5000);
        } catch (error) {
          messageDiv.textContent = "Failed to remove participant. Please try again.";
          messageDiv.className = "error";
          messageDiv.classList.remove("hidden");
          setTimeout(() => {
            messageDiv.classList.add("hidden");
          }, 5000);
          console.error("Error removing participant:", error);
        }
      });
    });
  }

  // Function to update activity card with new participant
  function updateActivityCard(activityCard, details) {
    const spotsLeft = details.max_participants - details.participants.length;
    activityCard.querySelector('p:nth-of-type(3)').innerHTML = `<strong>Availability:</strong> ${spotsLeft} spots left`;
    const participantsList = activityCard.querySelector('.participants ul');
    participantsList.innerHTML = details.participants.map(participant => `<li>${participant} <button class="remove-btn" data-email="${participant}" data-activity="${activityCard.dataset.activityName}">X</button></li>`).join('');
    // Re-attach event listeners for remove buttons
    attachRemoveListeners(activityCard);
  }

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${details.max_participants - details.participants.length} spots left</p>
          <div class="participants">
            <strong>Participants:</strong>
            <ul>
              ${details.participants.map(participant => `<li>${participant} <button class="remove-btn" data-email="${participant}" data-activity="${name}">X</button></li>`).join('')}
            </ul>
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Attach event listeners to remove buttons
        attachRemoveListeners(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);

        // Store reference to the activity card for later updates
        activityCard.dataset.activityName = name;
        activityCard.dataset.activityDetails = JSON.stringify(details);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();

        // Update the corresponding activity card
        const activityCard = Array.from(activitiesList.children).find(card => card.querySelector('h4').textContent === activity);
        if (activityCard) {
          // Update the stored details by adding the new participant
          const currentDetails = JSON.parse(activityCard.dataset.activityDetails);
          const updatedDetails = {
            ...currentDetails,
            participants: [...currentDetails.participants, email]
          };
          updateActivityCard(activityCard, updatedDetails);
          activityCard.dataset.activityDetails = JSON.stringify(updatedDetails); // Update stored details
        }
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
