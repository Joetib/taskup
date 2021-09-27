<template>
  <div id="id_11" class="container-fluid h-min-100vh">
    <div class="row h-min-100vh">
      <side-panel id="id_10"></side-panel>
      <div class="col-sm-9 col-md-9 col-lg-9 col-xl-10 px-0 px-md-2">
        <div class="row">
          <div class="col-lg-8 px-0 px-md-2">
            <div class="container py-4">
              <router-link :to="project_link">
                <h5>{{ task.project.name }}</h5>
              </router-link>

              <div class="pt-2 pb-2">
                <div
                  class="
                    d-flex
                    flex-column flex-md-row
                    justify-content-md-between
                  "
                >
                  <div>
                    <h2>{{ task.name }}</h2>
                    <span
                      class="badge pill mb-3"
                      v-bind:class="{
                        'bg-danger': isNotStarted,
                        'bg-primary': isInProgress,
                        'bg-success': isCompleted,
                      }"
                    >
                      {{ completion_status }}
                    </span>
                  </div>
                  <div
                    class="
                      d-flex
                      flex-row flex-md-column
                      align-items-md-end
                      flex-wrap
                    "
                  >
                    <div>
                      <button
                        v-if="isNotStarted"
                        @click="update_status('In Progress')"
                        class="btn btn-warning my-1 mx-1"
                      >
                        Mark as In Progress
                      </button>
                    </div>
                    <div>
                      <button
                        v-if="isInProgress"
                        @click="update_status('Completed')"
                        class="btn btn-warning my-1 mx-1"
                      >
                        Mark as Completed
                      </button>
                    </div>
                    <div v-if="is_project_manager">
                      <button
                        @click="enable_edit_task_dialog"
                        class="btn btn-warning my-1 mx-1"
                      >
                        Edit
                      </button>
                    </div>
                    <div v-if="is_project_manager">
                      <DeleteTaskButton
                        v-bind:project_id="project_id"
                        v-bind:task_id="task_id"
                      ></DeleteTaskButton>
                    </div>
                  </div>
                </div>
              </div>
              <div class="bg-light p-4">
                {{ task.description }}
              </div>
            </div>

            <div class="container">
              <div class="row bg-white">
                <div class="col-12 bg-dark text-light py-2">
                  <div class="container">
                    <h4>Discussion</h4>
                  </div>
                </div>
                <div class="col-12">
                  <div class="container">
                    <div class="row">
                      <MessageCard
                        v-for="message in task.messages"
                        :key="message.id"
                        :message="message"
                      />
                      <div
                        class="
                          col-12
                          border border-start-0 border-end-0 border-bottom-0
                          mt-5
                        "
                      >
                        <CreateMessage
                          v-bind:project_id="project_id"
                          v-bind:task_id="task_id"
                          @create_message_done="create_message_done"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-lg-4 p-1">
            <div class="container-fluid py-5">
              <div class="mb-5">
                <h4>Manager</h4>
                <div v-if="task.project.manager">
                  <h5 class="m-0">{{ task.project.manager.name }}</h5>
                  <small>{{ task.project.manager.email }}</small>
                </div>
              </div>
              <TaskContribution
                :project_id="project_id"
                :task_id="task_id"
              ></TaskContribution>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div
      class="full-screen-form-overlay"
      v-if="is_project_manager && open_edit_task_dialog"
    >
      <edit-task
        v-bind:project_id="project_id"
        v-bind:task_id="task_id"
        v-bind:task_name="task.name"
        v-bind:task_description="task.description"
        @edit_task_done="edit_task_done"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CreateMessage from "../components/CreateMessage.vue";
import MessageCard from "../components/MessageCard.vue";
import DeleteTaskButton from "../components/DeleteTaskButton.vue";
import TaskContribution from "../components/TaskContribution.vue";
import SidePanel from "../components/SidePanel.vue";
import EditTask from "../components/EditTask.vue";
export default {
  components: {
    CreateMessage,
    MessageCard,
    DeleteTaskButton,
    TaskContribution,
    SidePanel,
    EditTask,
  },
  data() {
    return {
      task: {
        name: "",
        description: "",
        project: {
          manager: { name: "name" },
        },
        is_project_manager: false,
      },
      open_create_message_dialog: false,
      open_edit_task_dialog: false,
    };
  },
  methods: {
    enable_edit_task_dialog() {
      this.open_edit_task_dialog = !this.open_edit_task_dialog;
    },
    edit_task_done() {
      this.fetchTask(this.project_id, this.task_id);
      this.open_edit_task_dialog = false;
    },
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
      this.$store.commit("setIsLoading", true);

      axios
        .get(`/project/${project_id}/task/${task_id}/`)
        .then((e) => {
          console.log(e.data);
          if (e.data.success) {
            this.task = e.data.result;
            this.is_project_manager = e.data.is_project_manager;
          } else {
            this.error = e.data.message;
          }
          this.$store.commit("setIsLoading", false);
        })
        .catch((e) => {
          console.log(e);
          this.error = "Sorry could not load task.";
          this.$store.commit("setIsLoading", false);
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
    project_link() {
      return `/project/${this.project_id}/`;
    },
  },
  mounted() {
    this.fetchTask(this.project_id, this.task_id);
  },
};
</script>

<style scoped>
@media screen and (max-width: 770px) {
  #id_10{
    display: none;
  }
}
#id_11{
  min-height: 100vh;
}
</style>