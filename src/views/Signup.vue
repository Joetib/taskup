<template>
  <div class="container py-5" style="max-width: 500px">
    <form @submit.prevent="signup">
      <div>
        <h3>Enter details to Sign Up</h3>
        <p class="lead">so we can show you that world you dream of...</p>
        <div class=" p-2 rounded btn btn-outline-danger text-danger" v-if="error">
          {{ error }}
        </div>
        <div class="form-group py-2">
          <label>Name</label>
          <input type="text" v-model="name" class="form-control" />
        </div>
        <div class="form-group py-2">
          <label>Email</label>
          <input type="email" v-model="email" class="form-control" placeholder="example@gmail.com" />
        </div>
        <div class="form-group py-2">
          <label>Password</label>
          <input type="password" v-model="password" class="form-control" />
        </div>
        <div class="form-group py-2">
          <button class="btn btn-primary" @click="signup">Sign Up</button>
        </div>
        <div class="form-group">
          <p>
            Kindly <router-link id="link1" to="/login">login</router-link> if you already
            have an account.
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
      name: "",
      password: "",
      email: "",
      error: "",
    };
  },
  methods: {
    signup() {
      if (!this.name.length > 3) {
        this.error = "Please enter a name.";
      }
      if (!this.email.length > 3) {
        this.error = "Please enter an email address.";
      } else if (this.password.length < 5) {
        this.error = "Password must be at least 5 characters long";
      } else {
        this.$store.commit("setIsLoading", true);
        axios
          .post("/auth/signup/", {
            name: this.name,
            email: this.email,
            password: this.password,
          })
          .then((e) => {
            if (e.data.success) {
              this.username = e.data.name;
              this.token = e.data.token;
              this.$store.commit("updateUsername", e.data.name);
              this.$store.commit("updateToken", e.data.token);
              this.$store.commit("updateEmail", e.data.email);
              this.$store.commit("setIsLoading", false);

              if (this.$route.params.nextUrl == null) {
                this.$router.push("/dashboard");
              } else {
                this.$router.push(this.$route.params.nextUrl);
              }
            }else {
                this.error = e.data.message;
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

<style scoped>
#link1{
  color: blue;
}
.btn-primary{
  border-radius: 15px;
  border: none;
}
.btn-primary:hover{
  background-color:rgb(95, 12, 95);
}

.container{
  border-radius: 2em;
  margin-top: 50px;
}

@media screen and (min-width: 770px) {
  .container{
  background-color:rgba(224, 46, 40, 0.267);
}
}
</style>