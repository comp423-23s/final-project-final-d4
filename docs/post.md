# Post

## Overview
The post forum feature provides functionality for viewing posts, creating posts, searching for posts, and deleting posts in the post forum. This feature fulfills **four** stories in our project, including view-post story, create-post story, search-post story, and delete-post story. It primarily serves to **UNC students who are looking for potential projects to get involved in or students who have project ideas in mind and are looking for teammates to build the project together**. 

This feature is the primary feature in our final project and would make the UNC CS community more cooperative and innovative. The four primary functions in this feature is:

* **View post**: All people can browse the post forum in the post tab after authentication. 
* **Create post**: A CSXL user could create a post by navigating to create-post in the post forum. The user should enter the post title, description, content, and choose tags to create a post. (Warning: only registered users can create post! This feature would be improved in the future.)
* **Search post**: CSXL user could search specific posts using the search bar on the top. 
* **Delete post**: CSXL users could delete their own posts in the post forum if they click on the red delete button. Administrator could delete all users' posts by clicking the gray delete button.

## Implementation Notes
This feature is associated with a post table (backend/entities/post_entities). Each post has features such as content, tags, created time, title, and descriptions. The title can be simple, such as "Finding teammate: backend" or "Random thoughts about ChatGPT". The descriptions are a brief summary of the post, for example, "I found this interesting paper on ChatGPT talking about its possible applications".

One of the interesting design points is tags. We thought about our experiences on other platforms and found that it is useful for viewers to find specific categories of posts they want if the author of a post can tag the post initially. For example, if a user wants to join an existing team for a project, the user can search for the tag "Finding teammates". Every post with this tag will appear, making it easier for the user to find what they are looking for. We have some predefined tags such as "finding teammates", "share insights", "backend", "frontend". We chose to use tags instead of letting users search posts by contents or titles because we understand that people would have different wording for the same thing. The tag can unify the wording and make it easier for users to retrieve the information they want.

## Development Concerns
**Please do not create a post if you have not yet registered in CSXL!** The create-post function depends on a registered user, and the action should result in a HTTP error if the user is not yet registered!

Other than that, if a developer wanted to start working on your post feature, be aware of the following things:
Backend: 
1. The backend implementation of the post forum feature is in api/post.py and services/post.py. The create_post service function takes a NewPost model from the frontend post form, which only has content, tags, created, datetime, title, and description. The create_post function will take parameters from the NewPost model and construct a Post model for passing into the post table. The Post model has information about the user who creates the post by extracting from the /authentication/registered user.
2. There is a permission check in the delete_post method. If the subject is not the user who created the post, the permission service would check whether the subject has permission to delete the post. Only the administrator who has the post.delete action permission would delete other users' posts.
Frontend:
1. The frontend implementation of the post feature is in the [post-list component](https://github.com/comp423-23s/final-project-final-d4/tree/stage/frontend/src/app/post-list), create-post component(https://github.com/comp423-23s/final-project-final-d4/tree/stage/frontend/src/app/create-post), and post.service.ts(https://github.com/comp423-23s/final-project-final-d4/blob/stage/frontend/src/app/post.service.ts). 
2. There are 2 permission checks in the delete post sub-feature of the frontend. **deleteAdminPermission$** is an Observable<Boolean> checks whether the authenticated user has permission to delete user people's posts. It interacts with the check method of the permission service to fetch permission information. [The delete button for administrator only appears if the boolean variable is true](https://github.com/comp423-23s/final-project-final-d4/blob/02ac2feea0af519d223566723c4170c53cffb076/frontend/src/app/post-list/post-list.component.html#L23). The second permission check is implemented via **getDeleteUserPermission** function. It takes the pid associated with the specific post and calls [checkPID(PID: number)](https://github.com/comp423-23s/final-project-final-d4/blob/02ac2feea0af519d223566723c4170c53cffb076/frontend/src/app/permission.service.ts#L29) in the permission service. This method returns true if the postPID and the PID of the CSXL user are equal. 
3. The create-post sub-feature sends the NewPost model to the backend via HTTP POST request. All methods with HTTP concerns in the post service takes PostView model as a return object. NewPost matches NewPost model in the backend while PostView Matches Post model in the backend. 

## Future Work
1. The create-post router-link should only appear if the user is registered via CSXL. If the user is not registered, clicking on the create-post button should redirect user to profile to create a new account. 