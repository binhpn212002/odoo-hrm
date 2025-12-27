/* @odoo-module */
// @ts-nocheck


import {patch} from "@web/core/utils/patch";
import {ThreadService} from "@mail/core/common/thread_service";
import {Record} from "@mail/core/common/record";

// const FETCH_LIMIT = 30;
// patch(ThreadService.prototype, {
//     async fetchMessages(thread, {after, before, message_chatter_type} = {}) {
//         thread.status = "loading";
//         if (thread.type === "chatter" && !thread.id) {
//             thread.isLoaded = true;
//             return [];
//         }
//         console.log("call fetch message", message_chatter_type)
//         try {
//             // ordered messages received: newest to oldest
//             const {messages: rawMessages} = await this.rpc(this.getFetchRoute(thread), {
//                 ...this.getFetchParams(thread),
//                 limit: FETCH_LIMIT,
//                 after,
//                 before, message_chatter_type
//             });
//             let messages = this.store.Message.insert(rawMessages.reverse(), {html: true});
//             //
//             // if (thread.type === "chatter") {
//             //     messages = this.store.Message.new(rawMessages.reverse(), {html: true});
//             //
//             // }
//             thread.isLoaded = true;
//             return messages;
//         } catch (e) {
//             thread.hasLoadingFailed = true;
//             throw e;
//         } finally {
//             thread.status = "ready";
//         }
//     },
//     async fetchNewMessages(thread, {message_chatter_type} = {}) {
//         if (
//             thread.status === "loading" ||
//             (thread.isLoaded && ["discuss.channel", "mail.box"].includes(thread.model))
//         ) {
//             return;
//         }
//         console.log("call fetchNewMessages", message_chatter_type)
//
//         const after = thread.isLoaded ? thread.newestPersistentMessage?.id : undefined;
//         try {
//             const fetched = await this.fetchMessages(thread, {after, message_chatter_type});
//             // feed messages
//             // could have received a new message as notification during fetch
//             // filter out already fetched (e.g. received as notification in the meantime)
//             let startIndex;
//             if (after === undefined) {
//                 startIndex = 0;
//             } else {
//                 const afterIndex = thread.messages.findIndex((message) => message.id === after);
//                 if (afterIndex === -1) {
//                     // there might have been a jump to message during RPC fetch.
//                     // Abort feeding messages as to not put holes in message list.
//                     return;
//                 } else {
//                     startIndex = afterIndex + 1;
//                 }
//             }
//             const alreadyKnownMessages = new Set(thread.messages.map((m) => m.id));
//             const filtered = fetched.filter(
//                 (message) =>
//                     !alreadyKnownMessages.has(message.id) &&
//                     (thread.persistentMessages.length === 0 ||
//                         message.id < thread.oldestPersistentMessage.id ||
//                         message.id > thread.newestPersistentMessage.id)
//             );
//             thread.messages.splice(startIndex, 0, ...filtered);
//             // feed needactions
//             // same for needaction messages, special case for mailbox:
//             // kinda "fetch new/more" with needactions on many origin threads at once
//             if (thread.eq(this.store.discuss.inbox)) {
//                 Record.MAKE_UPDATE(() => {
//                     for (const message of fetched) {
//                         const thread = message.originThread;
//                         if (thread && message.notIn(thread.needactionMessages)) {
//                             thread.needactionMessages.unshift(message);
//                         }
//                     }
//                 });
//             } else {
//                 const startNeedactionIndex =
//                     after === undefined
//                         ? 0
//                         : thread.messages.findIndex((message) => message.id === after);
//                 const filteredNeedaction = fetched.filter(
//                     (message) =>
//                         message.isNeedaction &&
//                         (thread.needactionMessages.length === 0 ||
//                             message.id < thread.needactionMessages[0].id ||
//                             message.id > thread.needactionMessages.at(-1).id)
//                 );
//                 thread.needactionMessages.splice(startNeedactionIndex, 0, ...filteredNeedaction);
//             }
//             Object.assign(thread, {
//                 loadOlder:
//                     after === undefined && fetched.length === FETCH_LIMIT
//                         ? true
//                         : after === undefined && fetched.length !== FETCH_LIMIT
//                             ? false
//                             : thread.loadOlder,
//             });
//         } catch {
//             // handled in fetchMessages
//         }
//     },
//     async fetchData(
//         thread,
//         requestList = ["activities", "followers", "attachments", "messages", "suggestedRecipients"], {message_chatter_type} = {}
//     ) {
//         console.log("call fetchData", message_chatter_type)
//         thread.isLoadingAttachments =
//             thread.isLoadingAttachments || requestList.includes("attachments");
//         if (requestList.includes("messages")) {
//             this.fetchNewMessages(thread, {message_chatter_type});
//         }
//         const result = await this.rpc("/mail/thread/data", {
//             request_list: requestList,
//             thread_id: thread.id,
//             thread_model: thread.model,
//         });
//         if ("attachments" in result) {
//             result["attachments"] = result["attachments"].map((attachment) => ({
//                 ...attachment,
//                 originThread: this.store.Thread.insert(attachment.originThread[0][1]),
//             }));
//         }
//         thread.canPostOnReadonly = result.canPostOnReadonly;
//         thread.hasReadAccess = result.hasReadAccess;
//         thread.hasWriteAccess = result.hasWriteAccess;
//         if ("activities" in result) {
//             const existingIds = new Set();
//             for (const activity of result.activities) {
//                 existingIds.add(this.store.Activity.insert(activity, {html: true}).id);
//             }
//             for (const activity of thread.activities) {
//                 if (!existingIds.has(activity.id)) {
//                     this.activityService.delete(activity);
//                 }
//             }
//         }
//         if ("attachments" in result) {
//             Object.assign(thread, {
//                 areAttachmentsLoaded: true,
//                 attachments: result.attachments,
//                 isLoadingAttachments: false,
//             });
//         }
//         if ("mainAttachment" in result) {
//             thread.mainAttachment = result.mainAttachment.id ? result.mainAttachment : undefined;
//         }
//         if (!thread.mainAttachment && thread.attachmentsInWebClientView.length > 0) {
//             this.setMainAttachmentFromIndex(thread, 0);
//         }
//         if ("followers" in result) {
//             if (result.selfFollower) {
//                 thread.selfFollower = {followedThread: thread, ...result.selfFollower};
//             }
//             thread.followersCount = result.followersCount;
//             Record.MAKE_UPDATE(() => {
//                 for (const followerData of result.followers) {
//                     const follower = this.store.Follower.insert({
//                         followedThread: thread,
//                         ...followerData,
//                     });
//                     if (follower.notEq(thread.selfFollower)) {
//                         thread.followers.add(follower);
//                     }
//                 }
//             });
//             thread.recipientsCount = result.recipientsCount;
//             for (const recipientData of result.recipients) {
//                 thread.recipients.add({followedThread: thread, ...recipientData});
//             }
//         }
//         if ("suggestedRecipients" in result) {
//             this.insertSuggestedRecipients(thread, result.suggestedRecipients);
//         }
//         return result;
//     },
// })