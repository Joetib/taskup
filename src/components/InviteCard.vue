<template>
  <div class="col-xl-4 col-6">
    <div class="shadow pjboard transition-2">
      <div class="card-body">
        <h5>{{ invite.project.name }}</h5>
        <p>{{ invite.project.description }}</p>
        <div class="row">
          <div class="col">
            <button @click="accept" class="btn btn-primary w-100 my-1">Accept</button>
          </div>
          <div class="col">
            <button @click="decline" class="btn btn-danger w-100 my-1">Decline</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
export default {
  props: {
    invite: null,
  },
  methods: {
    accept() {
      axios.get(`/invitation/${this.invite.id}/accept/`).then((e) => {
        if (e.data.success) {
          this.$router.push(`/project/${this.invite.project_id}/`);
        }
      });
    },
    decline() {
      axios.get(`/invitation/${this.invite.id}/decline/`).then((e) => {
        if (e.data.success) {
          this.$router.push(`/invites/`);
          this.$emit('deleted');
        }
      });
    },
  },
};
</script>

<style scoped>
@media screen and (min-width: 770px) {
.pjboard:hover,.pjboard:active{
  transform: translateY(-5px);
  box-shadow: 0 0 20px 5px rgb(161, 77, 77,0.5) !important;
}
}
</style>