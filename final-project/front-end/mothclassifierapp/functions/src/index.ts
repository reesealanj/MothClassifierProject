import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';
admin.initializeApp();

const fcm = admin.messaging();

// Send a notification to ONE device at a time
export const sendToDevice = functions.firestore
    // will fire when a notification document is created
    .document('notifications/{notificationID}')
    .onCreate(async snapshot => {
        const notiData = snapshot.data();

        const notiPayload: admin.messaging.MessagingPayload = {
            notification: {
                title: `${notiData.title}`,
                body: `${notiData.body}`,
                clickAction: 'FLUTTER_NOTIFICATION_CLICK',
            },
        };

        return fcm.sendToDevice(notiData.app_token, notiPayload);
    });