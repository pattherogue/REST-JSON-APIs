// Define the base URL for the API
const BASE_URL = "http://localhost:5000/api";

/** 
 * Given data about a cupcake, generate HTML representation of the cupcake.
 * @param {Object} cupcake - Cupcake data
 * @returns {string} HTML representation of the cupcake
 */
function generateCupcakeHTML(cupcake) {
  return `
    <div class="cupcake" data-cupcake-id="${cupcake.id}">
      <li>
        Flavor: ${cupcake.flavor} / Size: ${cupcake.size} / Rating: ${cupcake.rating}
        <button class="edit-button">Edit</button>
        <button class="delete-button">Delete</button>
      </li>
      <img class="Cupcake-img"
            src="${cupcake.image}"
            alt="Cupcake Image">
    </div>
  `;
}

/** 
 * Put initial cupcakes on the page.
 */
async function showInitialCupcakes() {
  try {
    // Fetch initial cupcakes data from the API
    const response = await axios.get(`${BASE_URL}/cupcakes`);

    // Iterate through each cupcake data and generate HTML for it
    for (let cupcakeData of response.data.cupcakes) {
      // Create a new jQuery object for the cupcake HTML and append it to the cupcakes list
      let newCupcake = $(generateCupcakeHTML(cupcakeData));
      $("#cupcakes-list").append(newCupcake);
    }
  } catch (error) {
    console.error("Error fetching cupcakes:", error);
    alert("Error fetching cupcakes. Please try again later.");
  }
}

/** 
 * Handle form submission for adding new cupcakes.
 */
$("#new-cupcake-form").on("submit", async function (evt) {
  evt.preventDefault();

  try {
    // Extract form input values
    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();

    // Send a POST request to add the new cupcake
    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
      flavor,
      rating,
      size,
      image
    });

    // Generate HTML for the new cupcake and append it to the cupcakes list
    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    // Reset the form fields
    $("#new-cupcake-form").trigger("reset");
    alert("Cupcake added successfully!");
  } catch (error) {
    console.error("Error adding cupcake:", error);
    alert("Error adding cupcake. Please try again later.");
  }
});

/** 
 * Handle click event for deleting a cupcake.
 */
$("#cupcakes-list").on("click", ".delete-button", async function (evt) {
  evt.preventDefault();
  // Find the closest cupcake div and extract its ID
  let $cupcake = $(evt.target).closest(".cupcake");
  let cupcakeId = $cupcake.attr("data-cupcake-id");
  try {
    // Send a DELETE request to delete the cupcake
    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    // Remove the cupcake HTML from the page
    $cupcake.remove();
    alert("Cupcake deleted successfully!");
  } catch (error) {
    console.error("Error deleting cupcake:", error);
    alert("Error deleting cupcake. Please try again later.");
  }
});

/** 
 * Handle click event for editing a cupcake.
 */
$("#cupcakes-list").on("click", ".edit-button", function (evt) {
  evt.preventDefault();
  // Find the closest cupcake div and extract its ID
  let $cupcake = $(evt.target).closest(".cupcake");
  let cupcakeId = $cupcake.attr("data-cupcake-id");
  // Get cupcake data
  let flavor = $cupcake.find("li").text().trim().split(" / ")[0];
  let size = $cupcake.find("li").text().trim().split(" / ")[1];
  let rating = $cupcake.find("li").text().trim().split(" / ")[2];
  let image = $cupcake.find("img").attr("src");
  // Pre-fill update form with cupcake data
  $("#edit-flavor").val(flavor);
  $("#edit-size").val(size);
  $("#edit-rating").val(rating);
  $("#edit-image").val(image);
  // Show the update form
  $("#update-cupcake-form").show().attr("data-cupcake-id", cupcakeId);
});

/** 
 * Handle form submission for updating a cupcake.
 */
$("#edit-cupcake-form").on("submit", async function (evt) {
  evt.preventDefault();
  // Extract form input values
  let cupcakeId = $("#update-cupcake-form").attr("data-cupcake-id");
  let flavor = $("#edit-flavor").val();
  let rating = $("#edit-rating").val();
  let size = $("#edit-size").val();
  let image = $("#edit-image").val();
  try {
    // Send a PATCH request to update the cupcake
    await axios.patch(`${BASE_URL}/cupcakes/${cupcakeId}`, {
      flavor,
      rating,
      size,
      image
    });
    // Hide the update form
    $("#update-cupcake-form").hide();
    // Refresh cupcakes list
    await showInitialCupcakes();
    alert("Cupcake updated successfully!");
  } catch (error) {
    console.error("Error updating cupcake:", error);
    alert("Error updating cupcake. Please try again later.");
  }
});

/** 
 * Handle click event for canceling update.
 */
$("#cancel-update").on("click", function (evt) {
  evt.preventDefault();
  // Hide the update form
  $("#update-cupcake-form").hide();
});

// Call the function to show initial cupcakes when the page loads
$(showInitialCupcakes);
