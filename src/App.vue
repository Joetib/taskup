<template>
  <div class="container-fluid">
    <div class="row h-min-100vh">
        <!-- <SidePanel /> -->
      <div class=" px-0" id="nav">
        <NavBar />
        <div class="loading sticky-top" v-if="$store.state.is_loading">
          <div class="circle-loader"></div>
          <span class="load-item"></span>
          <span class="load-item"></span>
          <span class="load-item"></span>
        </div>
        <router-view />
      </div>
    </div>
  </div>
</template>
<script>
import NavBar from "./components/NavBar.vue";
// import SidePanel from "./components/SidePanel.vue";
export default {
  name: "App",
  components: {
    NavBar,
   // SidePanel,
  },
  beforeCreate() {
    this.$store.commit("initializeStore");
  },
};
 
 window.addEventListener("click",function(){
    var button = document.querySelector('#btoggle')
   if(!button.classList.contains("collapsed"))
     button.click()
 })
</script>


<style>
@import url("https://fonts.googleapis.com/css?family=Sofia&effect=emboss|Rampart+One&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Rampart+One&display=swap");

:root{
  --accent-color:rgb(114, 198, 250);
  --custom-font: 'Rampart One', cursive;
  --taskup-font: "Sofia", sans-serif; 
}

body{
  background-color: #0e08081e;
  height: 200vh; /* You must set a specified height */
  background-position: center; /* Center the image */
  background-repeat: no-repeat; /* Do not repeat the image */
  background-size: cover; /* Resize the background image to cover the entire container */
}


.row{
  height: 1500px;
}
.pointer {
  cursor: pointer;
}
.bg-dark-2 {
  background: #333;
}
.bg-dark-3 {
  background: #444;
}

@keyframes loading {
  0% {
    background: gold;
  }
  70% {
    background: #555;
  }
}
.load-item {
  border-radius: 50%;
  padding: 10px;
  width: 10px;
  height: 10px;
  background: #555;
  margin: 20px;
  animation: loading 0.9s ease-in infinite;
}
.load-item:nth-child(1) {
  animation-delay: 0s;
}
.load-item:nth-child(2) {
  animation-delay: 0.3s;
}
.load-item:nth-child(3) {
  animation-delay: 0.6s;
}
.loading {
  display: flex;
  justify-content: center;
  align-items: center;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.circle-loader {
  border: 16px solid rgb(68, 59, 9);
  border-top: 16px solid #666;
  border-radius: 50%;
  width: 120px;
  height: 120px;
  animation: spin 2s linear infinite;
}
.h-min-100vh{
  min-height: 100vh;
}
a {
  text-decoration: none;
  color: unset;
}
a:hover {
  color: unset;
}
</style>
