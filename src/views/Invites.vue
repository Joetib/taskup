<template>
  <div id="id_11" class="container-fluid h-min-100vh">
    <div class="row h-min-100vh">
      <side-panel id="id_10"></side-panel>
      <div class="col-sm-9 col-md-9 col-lg-9 col-xl-10">
        <div class="container py-5">
            <h1 class="pb-3">Invites</h1>

          <div class="row">
            <InviteCard
              @deleted="fetch_invites"
              v-for="invite in invites"
              :invite="invite"
              :key="invite.id"
              class="col-xl-4 col-12"
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
@media screen and (max-width: 770px) {
  #id_10{
    display: none;
  }
}
#id_11{
  min-height: 100vh;
}
</style>