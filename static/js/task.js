function taskData(projectId) {
    return {
        tasks: [],
        moveTask(taskIndex, direction) {
            const currentTask = this.tasks[taskIndex];
            const neighborTask = this.tasks[taskIndex + direction];

            if (neighborTask) {
                [currentTask.priority, neighborTask.priority] = [neighborTask.priority, currentTask.priority];

                this.updateTaskPriority(currentTask.id, currentTask.priority);
                this.updateTaskPriority(neighborTask.id, neighborTask.priority);

                const temp = this.tasks[taskIndex + direction];
                this.tasks[taskIndex + direction] = this.tasks[taskIndex];
                this.tasks[taskIndex] = temp;
            }
        },

        updateTaskPriority(taskId, priority) {
            htmx.ajax('PATCH', `/projects/${projectId}/tasks/${taskId}/`, {
                values: {priority},
                swap: 'none'
            });
        }
    };
}
