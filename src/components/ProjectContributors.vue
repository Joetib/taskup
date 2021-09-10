<template>
  <div class="container-fluid bg-white py-3">
    <h4>Contributors</h4>
    <hr />
    <p class="text-danger">{{ error_message }}</p>
    <div v-if="is_project_manager">
      <input
        type="text"
        v-model="selected_user"
        list="users_list"
        placeholder="search user"
        class="form-control"
      />
      {{ selected_user }}
      <datalist id="users_list">
        <option
          v-for="user in all_users"
          :key="user.id"
          :value="user.email"
          @click="set_selected_user(user.id)"
        >
          {{ user.name }} ({{ user.email }})
        </option>
      </datalist>
      <!-- <select list="users_list" v-model="selected_user"  class="form-select">
        <option  v-for="user in all_users" :key="user.id" :value="user.id">
          {{ user.name }} ({{ user.email }})
        </option>
      </select> -->

      <button @click="add_selected_user" class="btn mt-2 w-100 btn-primary">
        Add
      </button>
    </div>
    <div class="" v-for="user in users" :key="user.id">
      <!-- <img
        src=""
        class="img-thumbnail rounded-circle"
        style="width: 60px; height: 60px"
      /> -->
      <div
        class="
          d-flex
          justify-content-between
          border border-top-0 border-start-0 border-end-0
          p-2
        "
      >
        <div>
          <h6 class="m-0">{{ user.name }}</h6>
          <small>{{ user.email }}</small>
        </div>
        <div v-if="is_project_manager">
          <button
            @click="remove_contributor([user.id])"
            class="btn btn-danger btn-sm"
          >
            <i class="fa fa-times"></i>
          </button>
        </div>
      </div>
    </div>
    <div class="pt-3 bg-light p-2" v-if="invites.length">
      <h5>Pending Invites</h5>
      <hr />
      <div class="" v-for="invite in invites" :key="invite.id">
        <div
          class="
            d-flex
            justify-content-between
            border border-top-0 border-start-0 border-end-0
            p-2
          "
        >
          <div>
            <h6 class="m-0">{{ invite.user.name }}</h6>
            <small>{{ invite.user.email }}</small>
          </div>
          <div>
            <button
              @click="cancel_invitation(invite.id)"
              class="btn btn-danger btn-sm"
            >
              <i class="fa fa-times"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      users: [],
      selected_user: null,
      all_users: [],
      invites: [],
      error_message: "",
    };
  },
  props: {
    project_id: null,
    is_project_manager: null,
  },
  methods: {
    remove_contributor(user_ids) {
      axios
        .post(`project/${this.project_id}/remove-contributor/`, {
          contributors: user_ids,
        })
        .then((e) => {
          if (e.data.success) {
            this.fetch_project_contributors();
          } else {
            this.error_message = e.data.message;
            console.log(e.data);
          }
        })
        .catch((e) => {
          this.error_message = "Could not remove contributor";
          console.log(e);
        });
    },
    cancel_invitation(invite_id) {
      axios.get(`/invitation/${invite_id}/decline/`).then((e) => {
        if (e.data.success) {
          this.fetch_project_contributors()
        } else {
          this.error_message = e.data.message
        }
      }).catch(e => {
        console.log(e);
        this.error_message = "Sorry could not cancel invitation.";
      });
    },
    add_selected_user() {
      if (this.selected_user) {
        if (isNaN(this.selected_user)) {
          this.selected_user_id = this.all_users.filter(
            (user) => user.email == this.selected_user
          )[0].id;
        }
        axios
          .post(`project/${this.project_id}/add-contributor/`, {
            contributors: [this.selected_user_id],
          })
          .then((e) => {
            if (e.data.success) {
              this.fetch_project_contributors();
            } else {
              this.error_message = e.data.message;
              console.log(e.data);
            }
          })
          .catch((e) => {
            this.error_message = "Could not add Contributor";
            console.log(e);
          });
      }
    },
    fetch_project_contributors() {
      axios
        .get(`project/${this.project_id}/contributors/`)
        .then((e) => {
          console.log(e.data);
          if (e.data.success) {
            this.users = e.data.results;
            this.invites = e.data.invites;

            this.all_users = e.data.all_users;
          } else {
            this.error_message = e.data.message;
          }
        })
        .catch((e) => {
          console.log(e);
          this.error_message = "Sorry could not load contributors";
          alert("An error occurred when fetching users");
        });
    },
  },
  mounted() {
    this.fetch_project_contributors();
  },
};
</script>

<style>
</style>