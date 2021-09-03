<template>
  <div class="col-sm-3 col-md-3 col-lg-3 col-xl-2 bg-white px-0">
    <button class="btn toggle-btn btn-dark d-block d-sm-none" @click="toggle_show">
      Toggle
      </button>
    <div class="side-panel"  v-bind:class="{ 'show': show,}">
    <div class="py-5 bg-primary text-light">
      <div class="container">
        <h3>{{ this.$store.state.username }}</h3>
        <p class="">{{ this.$store.state.email }}</p>
      </div>
    </div>
    <div class="container h-100 px-2 pt-5">
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
          >Dashboard</router-link
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
          >Tasks</router-link
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
          >Invites</router-link
        >
        <router-link
          to="/"
          class="
            py-2
            border border-start-0 border-end-0 border-top-0
            d-block
            py-3
            nav-item nav-link
          "
          >Home</router-link
        >
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
@media only screen and (max-width: 576px) {
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
</style>