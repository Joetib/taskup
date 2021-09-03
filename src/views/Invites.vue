<template>
  <div class="container-fluid h-min-100vh">
    <div class="row h-min-100vh">
      <side-panel></side-panel>
      <div class="col-sm-9 col-md-9 col-lg-9 col-xl-10">
        <div class="container py-5">
          <div class="row">
            <div class="col-12 pt-3 pb-4">
              <h2>Pending Invites</h2>
            </div>
            <InviteCard
              @deleted="fetch_invites"
              v-for="invite in invites"
              :invite="invite"
              :key="invite.id"
              class="col-xl-4 col-6"
            >
            </InviteCard>

            <div v-if="!invites.length" class="col-12 py-3">
              <p class="text-danger">You have no pending invites.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import InviteCard from "../components/InviteCard.vue";
import SidePanel from "../components/SidePanel.vue";

export default {
  components: {
    InviteCard,
    SidePanel,
  },
  data() {
    return {
      invites: [],
      error_message: "",
    };
  },
  methods: {
    fetch_invites() {
      axios
        .get("/invitation/")
        .then((e) => {
          if (e.data.success) {
            this.invites = e.data.result;
          } else {
            this.error_message = e.data.message;
          }
        })
        .catch((e) => {
          console.log(e);
          this.error_message = "Could not load invites";
        });
    },
  },
  mounted() {
    this.fetch_invites();
  },
};
</script>

<style>
</style>