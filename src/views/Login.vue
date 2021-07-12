<template>
  <div class="container py-5" style="max-width: 500px">
    <form @submit.prevent="login">
      <div>
        <h3>Enter details to Log In</h3>
        <p class="lead">so we can show you that world you dream of...</p>
        <div class="text-danger py-2">
          {{ error }}
        </div>

        <div class="form-group py-2">
          <label>Email</label>
          <input type="email" v-model="email" class="form-control" />
        </div>
        <div class="form-group py-2">
          <label>Password</label>
          <input type="password" v-model="password" class="form-control" />
        </div>
        <div class="form-group py-2">
          <button class="btn btn-primary" @click="login">Login</button>
        </div>
        <div class="form-group">
          <p>
            Kindly <router-link to="/signup">signup</router-link> if you do not
            already have an account.
          </p>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",
  components: {},
  data() {
    return {
      password: "",
      email: "",
      error: ""
    };
  },
  methods: {
    login() {
      if (!this.email.length > 3) {
        this.error = "Please enter an email address.";
      } else if (this.password.length < 5) {
        this.error = "Password must be at least 5 characters long";
      } else {
        this.$store.commit("setIsLoading", true);
        axios
          .post("/auth/login/", {
            email: this.email,
            password: this.password,
          })
          .then((e) => {
            if (e.data.success) {
              this.username = e.data.name;
              this.token = e.data.token;
              this.$store.commit("updateUsername", e.data.name);
              this.$store.commit("updateToken", e.data.token);
              this.$store.commit("setIsLoading", false);

              if (this.$route.params.nextUrl == null) {
                this.$router.push("/dashboard");
              } else {
                this.$router.push(this.$route.params.nextUrl);
              }
            } else {
              this.error = e.data.message;
              this.$store.commit("setIsLoading", false);

            }
          })
          .catch((e) => {
            this.error =
              "Sorry that didn't work, check if your username and password are correct.";
            console.log(e);
            this.$store.commit("setIsLoading", false);
          });
      }
    },
  },
};
</script>

<style>
</style>