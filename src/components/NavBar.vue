<template>
  <nav class="navbar navbar-expand-md navbar-light transition sticky-top">
    <div class="container p-0">
      <router-link
        class="navbar-brand font-effect-emboss"
        to="/"
        onclick="window.location='#top'"
        ><img src="./../assets/logo.png" alt="" />TaskUp</router-link
      >
      <button
        class="navbar-toggler collapsed"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
        id="btoggle"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse p-1" id="navbarSupportedContent">
        <div class="ms-md-auto">
          <ul class="navbar-nav" :class="applyFix">
            <li class="nav-item">
              <router-link
                class="nav-link"
                aria-current="page"
                to="/"
                @click="toggle"
                onclick="window.location='#top'"
                >Home</router-link
              >
            </li>
            <li class="nav-link fix">|</li>

            <li class="nav-item">
              <router-link class="nav-link" to="/about" @click="toggle"
                >About Us</router-link
              >
            </li>
          </ul>
        </div>
        <ul class="navbar-nav ms-md-auto">
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link class="nav-link" to="/login" @click="toggle"
              >Log In</router-link
            >
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link class="nav-link" to="/signup" @click="toggle"
              >Sign Up</router-link
            >
          </li>
          <li class="nav-item" v-if="dashboardFix">
            <router-link class="nav-link" to="/dashboard" @click="toggle"
              >Dashboard/Projects</router-link
            >
          </li>
          <!-- <li class="nav-item" v-if="mobileMenuDisplay">
            <router-link class="nav-link" to="/dashboard" @click="toggle"
              >Dashboard/Projects</router-link
            >
          </li> -->
          <li class="nav-item" v-if="mobileMenuDisplay">
            <router-link class="nav-link" to="/tasks/" @click="toggle"
              >Tasks</router-link
            >
          </li>
          <li class="nav-item" v-if="mobileMenuDisplay">
            <router-link class="nav-link" to="/invites/" @click="toggle"
              >Invites</router-link
            >
          </li>
          <li class="nav-item ms-md-auto" v-if="isLoggedIn">
            <a
              @click="logout"
              class="nav-link text-white btn btn-sm btn-danger"
              id="logoutBtn"
              >Log Out</a
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
export default {
  name: "NavBar",
  data(){
    return {windowWidth: "",};
  },
  beforeCreate() {
    this.$store.commit("initializeStore");
  },
  created() {
    window.addEventListener("resize", this.setWindowWidth);
    console.log("setting event")
  },
  computed: {
    isLoggedIn() {
      return this.$store.state.token !== null && this.$store.state.token !== "";
    },
    applyFix() {
      if (this.isLoggedIn) return "applifix";
      return "";
    },
    mobileMenuDisplay() {
      console.log("checking resizes")
      
      return (
        this.isLoggedIn && this.windowWidth &&
        window.matchMedia("screen and (max-width: 770px)").matches
      );
    },
    dashboardFix() {
      if (this.isLoggedIn){
        return true;
      }
      return false;
      
    },
  },
  methods: {
    setWindowWidth(){
      this.windowWidth = window.innerWidth
      console.log("setting window width")
    },
    logout() {
      this.$store.commit("logout");
      this.$router.push("/");
      this.toggle();
    },
    toggle() {
      if (window.matchMedia("screen and (max-width: 770px)").matches)
        document.querySelector("#btoggle").click();
    },
  },
};
</script>

<style scoped>
.navbar-brand {
  font-weight: bolder;
  padding-left: 15px;
  font-size: 28px;
  font-family: var(--taskup-font);
}

.navbar-toggler {
  margin-right: 1em !important;
}

@media screen and (max-width: 770px) {
  .fix {
    display: none;
  }
}

#logoutBtn {
  font-weight: bolder;
  font-size: 1em;
}
@media screen and (min-width: 770px) {
  #logoutBtn {
    margin-left: 2em;
  }
  .applifix {
    margin-left: 65px !important;
  }
}

.navbar-nav .router-link-exact-active {
  color: var(--accent-color) !important;
}

@media screen and (min-width: 770px) {
  .navbar-nav .router-link-exact-active {
    color: var(--accent-color) !important;
    border-bottom: var(--accent-color) solid 2px;
    border-bottom-right-radius: 1em;
  }
  .navbar-nav {
    margin-left: -100px;
  }
}

#navbarSupportedContent {
  font-weight: bolder;
}

@media screen and (max-width: 770px) {
  #navbarSupportedContent {
    padding-left: 20px !important;
  }
}

img {
  margin: 0 10px 10px 0;
  height: 40px;
}
</style>