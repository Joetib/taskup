<template>
  <div class="col-sm-3 col-md-3 col-lg-3 col-xl-2 px-0 pnel">
    <div class="side-panel"  v-bind:class="{ 'show': show}">
      <div class="container text-truncate" style="font-weight:bold;text-align:center;color:#2e2d2de0">
        <h3>{{ this.$store.state.username }}</h3>
        <p class="text-truncate">{{ this.$store.state.email }}</p>
    </div>
    <div class="container h-100 px-2 pt-5" style="font-weight:bold;" id="id_7">
      <nav>
        <router-link
          to="/dashboard/"
          class="
            py-2
            border border-start-0 border-end-0 border-top-0
            d-block
            py-3
            nav-item nav-link
          "
          ><i class="fas fa-project-diagram pe-2"></i>Projects</router-link
        >
        <router-link
          to="/tasks/"
          class="
            py-2
            border border-start-0 border-end-0 border-top-0
            d-block
            py-3
            nav-item nav-link
          "
          ><i class="fas fa-tasks pe-2"></i>Tasks</router-link
        >
        <router-link
          to="/invites/"
          class="
            py-2
            border border-start-0 border-end-0 border-top-0
            d-block
            py-3
            nav-item nav-link
          "
          ><i class="fas fa-user-friends pe-2"></i>Invites</router-link>
      </nav>
    </div>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return {
      show: false,
    }
  },
  methods : {
    toggle_show(){
      this.show = !this.show;
    }
  },
};
</script>

<style>
@media only screen and (max-width: 770px) {
  .toggle-btn{
    position: fixed;
    left: 0px;
    top: 80px;
    z-index: 2
  }
  .side-panel {
    display: none;
  }
  .side-panel.show {
    display: block;
    animation: showanimation 0.6s ease-in-out;
  }
  @keyframes showanimation {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
    
  }
}

.pnel{
min-height:100vh;
background:rgba(15, 170, 231, 0.144);
background-image: linear-gradient(to left,rgba(15, 170, 231, 0), rgba(45, 110, 126, 0.4));
padding: 2em;
border-radius: 0 .8em 0 0;
}

#id_7:hover,#id_7:active{
 color:rgb(161, 77, 77);
}
</style>