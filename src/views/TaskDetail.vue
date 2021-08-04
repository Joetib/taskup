<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar start -->
      <div class="col-md-3 col-lg-2 pt-5">
        <div class="container">
          <ul class="list-unstyled">
            <li class="py-2">
              <a class="nav-link d-flex align-items-center gap-2" href="#">
                <i class="fa fa-file"></i> Dashboard
              </a>
            </li>
            <li class="py-2">
              <a class="nav-link d-flex align-items-center gap-2" href="#">
                <i class="fa fa-comment-alt"></i> Chats
              </a>
            </li>
          </ul>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Minus alias
          aut iusto consequuntur ex eaque, neque quia delectus explicabo
          distinctio, nesciunt inventore a culpa labore sint temporibus ipsam
          omnis at?
        </div>
      </div>
      <!-- Sidebar end -->
      <div class="col-lg-8">
<<<<<<< HEAD
=======
        <div class="container py-5">
          <DeleteTaskButton v-bind:project_id="project_id" v-bind:task_id="task_id"></DeleteTaskButton>
          <h2>{{ task.name }} </h2>
          <p>{{ task.description }}</p>
        </div>
>>>>>>> 9712bf03eed0e76fef79a8c103910376168bf4c4
        <div class="container">
          <router-link :to="project_link">
            <h3>{{ task.project.name }}</h3>
            </router-link>
          <hr>
        <div class=" py-5 d-flex justify-content-between">
          <div>
            <h2>{{ task.name }}</h2>
            <p>{{ task.description }}</p>
          </div>
          <div class="d-flex flex-column">
            <span
              class="badge mb-3"
              v-bind:class="{
                'bg-danger': isNotStarted,
                'bg-primary': isInProgress,
                'bg-success': isCompleted,
              }"
            >
              {{ completion_status }}
            </span>
            <button
              v-if="isNotStarted"
              @click="update_status('In Progress')"
              class="btn btn-warning"
            >
              Mark as In Progres
            </button>
            <button
              v-if="isInProgress"
              @click="update_status('Completed')"
              class="btn btn-warning"
            >
              Mark as Completed
            </button>
          </div>
        </div>
        </div>

        <div class="container">
          <div class="row py-4">
            <div class="col-12">
              <h2>Discussion</h2>
            </div>
            <div class="col-12">
              <CreateMessage
                v-bind:project_id="project_id"
                v-bind:task_id="task_id"
                @create_message_done="create_message_done"
              />
            </div>
            <MessageCard
              v-for="message in task.messages"
              :key="message.id"
              :message="message"
            />
          </div>
        </div>
      </div>
      <div class="col-lg-2 p-1">
        <div class="container-fluid py-5">
          <div class="mb-5">
            <h4>Manager</h4>
            <div v-if="task.project.manager">
              <h5 class="m-0">{{ task.project.manager.name }}</h5>
              <small>{{ task.project.manager.email }}</small>
            </div>
          </div>
          <h4>Contributors</h4>
          <div>
      <select v-model="selected_user" list="users-list" class="form-select">
        <option  v-for="user in task.project.contributors" :key="user.id" :value="user.id">
          {{ user.name }} ({{ user.email }})
        </option>
      </select>

      <button @click="add_selected_user" class="btn mt-2 w-100 btn-primary">Add</button>
    </div>
          <div
            class="card my-3"
            v-for="contributor in task.project.contributors"
            v-bind:key="contributor.id"
          >
            <div class="card-body">
              <h5 class="m-0">{{ contributor.name }}</h5>
              <small>{{ contributor.email }}</small>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="full-screen-form-overlay" v-if="open_create_message_dialog">
      <CreateMessage
        v-bind:project_id="project_id"
        v-bind:task_id="task_id"
        @create_message_done="create_message_done"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CreateMessage from "../components/CreateMessage.vue";
import MessageCard from "../components/MessageCard.vue";
import DeleteTaskButton from '../components/DeleteTaskButton.vue';

export default {
  components: {
    CreateMessage,
    MessageCard,
<<<<<<< HEAD
=======
    DeleteTaskButton,
    
>>>>>>> 9712bf03eed0e76fef79a8c103910376168bf4c4
  },
  data() {
    return {
      task: {
        name: "",
        project: {
          manager: { name: "name" },
        },
      },
      open_create_message_dialog: false,
    };
  },
  methods: {
    update_status(message) {
      axios
        .put(
          `/project/${this.project_id}/task/${this.task_id}/completion-status/`,
          { completion_status: message }
        )
        .then((e) => {
          if (e.data.success) {
            this.fetchTask(this.project_id, this.task_id);
          } else {
            this.error = e.data.message;
          }
        })
        .catch((e) => {
          console.log(e);
          this.error = "Sorry could not update status.";
        });
    },
    fetchTask(project_id, task_id) {
      axios.get(`/project/${project_id}/task/${task_id}/`).then((e) => {
        console.log(e.data);
        if (e.data.success) {
          this.task = e.data.result;
        } else {
          this.error = e.data.message;
        }
      });
    },
    create_message_done() {
      this.open_create_message_dialog = false;

      this.fetchTask(this.project_id, this.task_id);
    },
    enable_create_message() {
      this.open_create_message_dialog = true;
    },
  },
  computed: {
    completion_status() {
      let status = this.task.completion_status;
      if (
        !(
          status == "Not Started" ||
          status == "In Progress" ||
          status == "Completed"
        )
      ) {
        status = "Not Started";
      }

      return status;
    },

    isCompleted() {
      return this.task.completion_status == "Completed";
    },
    isInProgress() {
      return this.task.completion_status == "In Progress";
    },
    isNotStarted() {
      return this.task.completion_status == "Not Started";
    },
    project_id() {
      if (this.task.project_id !== null && this.task.project_id !== undefined) {
        return this.task.project_id;
      }
      return this.$route.params.project_id;
    },
    task_id() {
      if (this.task.id !== null && this.task.id !== undefined) {
        return this.task.id;
      }
      return this.$route.params.task_id;
    },
    project_link(){
      return `/project/${this.project_id}/`
    }
  },
  mounted() {
    this.fetchTask(this.project_id, this.task_id);
  },
};
</script>

<style>
</style>