import Foundation
import UserNotifications



class alarmManager: ObservableObject {
    private var webSocketTask: URLSessionWebSocketTask?
    @Published var isConnected = false
    
    
    func requestNotificationPermission() {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { success, error in
            if success {
                print("Notifications authorized")
            } else if let error = error {
                print("Notification error: \(error.localizedDescription)")
            }
        }
    }
    init() {
            requestNotificationPermission()
        }

    func triggerLocalNotification(title: String, body: String) {
        // 1. Create the content object (Note the spelling: Mutable)
        let notificationContent = UNMutableNotificationContent()
        notificationContent.title = title
        notificationContent.body = body
        notificationContent.sound = .default

        // 2. Create the trigger (fire in 1 second)
        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 1, repeats: false)
        
        // 3. Create the request
        let request = UNNotificationRequest(
            identifier: UUID().uuidString,
            content: notificationContent,
            trigger: trigger
        )
        
        // 4. Add the request to the notification center
        UNUserNotificationCenter.current().add(request) { error in
            if let error = error {
                print("Error scheduling notification: \(error.localizedDescription)")
            }
        }
    }
    func connect() {
        let ngrokUrl = "ca747afc10c7.ngrok-free.app" // Match your Python test ID
        guard let url = URL(string: "wss://\(ngrokUrl)/ws") else { return }
        
        var request = URLRequest(url: url)
        request.addValue("true", forHTTPHeaderField: "ngrok-skip-browser-warning")
        request.addValue("https://\(ngrokUrl)", forHTTPHeaderField: "Origin")
        
        let session = URLSession(configuration: .default)
        webSocketTask = session.webSocketTask(with: request)
        webSocketTask?.resume()
        
        print("Connected to \(url)")
        
        // 1. Immediately send the "Hello" message (like your Python script)
        self.sendMessage("Hello from SwiftUI client!")
        
        // 2. Start the recursive listener loop
        print("hokey tokey")
        self.receiveMessage()
        print("sokey woke")
        
        DispatchQueue.main.async {
            self.isConnected = true
        }
        webSocketTask?.resume()

        // ADD THIS: Send a ping to the server
        webSocketTask?.sendPing { error in
            if let error = error {
                print("Ping failed: \(error.localizedDescription)")
            } else {
                print("Ping successful! The connection is definitely alive.")
            }
        }
        
        receiveMessage()
    }
    
    func disconnect() {
        webSocketTask?.cancel()
        isConnected = false
        
    }
    
    // This replicates: await websocket.send("...")
    func sendMessage(_ text: String) {
        let message = URLSessionWebSocketTask.Message.string(text)
        webSocketTask?.send(message) { error in
            if let error = error {
                print("Send error: \(error)")
            }
        }
    }
    
    // This replicates: while True: message = await websocket.recv()
    private func receiveMessage() {
        print("stupid toke")
        let currentDate = Date()
        webSocketTask?.receive { [weak self] result in
            print(result)
            switch result {
            case .success(let message):
                switch message {
                case .string(let text):
                    print("Server says: \(text)")
                    if(text.contains("Warning")) {
                        self?.triggerLocalNotification(title: "⚠️ Alarm Alert", body: text)
                    }
                    
                default:
                    print("nopey")
                    break
                }
                let formatter = DateFormatter()
                formatter.dateFormat = "MM/dd/yyyy HH:mm:ss"
                var dateString = formatter.string(from: Date())

                // 3. Send it back to the server
                
                self?.sendMessage("Hello back from SwiftUI!: \(currentDate)")
                // RECURSION: This is how we keep the "While True" loop going in Swift
                print("seee he")
                self?.receiveMessage()
                
            case .failure(let error):
                print("Connection failed: \(error)")
                DispatchQueue.main.async { self?.isConnected = false }
            }
        }
        print("clocke?")
    }
}
