<template>
  <div id="top">
    <div class="h-min-100vh">
      <div class=" px-0" id="nav">
        <NavBar />
        <div class="loading sticky-top" v-if="$store.state.is_loading" >
          <span class="load-item"></span>
          <span class="load-item"></span>
          <span class="load-item"></span>
        </div>
        <router-view />
        <Footer />
      </div>
    </div>
  </div>
</template>


<script>
import NavBar from "./components/NavBar.vue";
import Footer from "./components/Footer.vue"




export default {
  name: "App",
  components: {
    NavBar,
    Footer
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

window.addEventListener('scroll', function(){
  var navbar = document.querySelector('.navbar')
  
    if(window.pageYOffset > 50){
       navbar.classList.add('shadow')
       navbar.classList.add('bg-light')
    }
    else {
       navbar.classList.remove('shadow')
       navbar.classList.remove('bg-light')
    }
});

</script>




<style>
@import url("https://fonts.googleapis.com/css?family=Sofia&effect=emboss|Rampart+One&display=swap");

:root{
  --accent-color:rgb(114, 198, 250);
  --custom-font: Arial, Helvetica, sans-serif;
  --taskup-font: "Sofia", sans-serif; 
}

.transition {    
  -webkit-transition: all 0.8s ease-in-out;
	-moz-transition: all 0.8s ease-in-out;
	-o-transition: all 0.8s ease-in-out;
	transition: all 0.8s ease-in-out;
}

.transition-2 {    
  -webkit-transition: all 0.4s ease-in-out;
	-moz-transition: all 0.4s ease-in-out;
	-o-transition: all 0.4s ease-in-out;
	transition: all 0.4s ease-in-out;
}

body{
  background-color:#f9f9f9;
}

/* Hide scrollbar for Chrome, Safari and Opera */
body::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
body {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  pointer-events: none;
  top: 60px;
  left: 0;
  right: 0;
}

.load-item {
  border-radius: 50%;
  padding: 10px;
  width: 10px;
  height: 10px;
  background: transparent;
  margin: 20px;
  animation: loading 0.6s ease-in-out infinite;
}

@keyframes loading {
  0% {
    background: rgb(230, 96, 96);
  }
  50% {
    background: rgb(204, 186, 82);
  }
  100%{
    background: rgb(124, 184, 75);
  }
}

.load-item:nth-child(1) {
  animation-delay: 0s;
}
.load-item:nth-child(2) {
  animation-delay: 0.3s;
}
.load-item:nth-child(3) {
  animation-delay: 0.5s;
}
a {
  color: unset;
  text-decoration: none;
}
a:hover{
  color: unset;
  text-decoration: none;

}
</style>
