//
//  SocketIOManager.swift
//  ClientChat
//
//  Created by Daniel Barbosa on 28/06/23.
//

import Foundation
import SocketIO

class SocketIOManager: NSObject {
    static let sharedInstance = SocketIOManager()
    
    lazy var manager = SocketManager(socketURL: URL(string: "http://localhost:8000")!, config: [.log(true), .compress])
    lazy var socket = manager.defaultSocket

    lazy var username = ""

    override init() {
        super.init()
    }
    
    func establishConnection() {
        socket.connect(withPayload: ["username": username])
    }
    
    func closeConnection() {
        socket.disconnect()
    }
    
    func sendMessage(message: String) {
        socket.emit("broadcast_chat_message", message)
    }
    
    func listenForMessages(completion: @escaping (String) -> Void) {
        socket.on("broadcast_chat_message") { (dataArray, socketAck) -> Void in
            completion(dataArray.first  as! String)
        }

        socket.on("client_count") { (dataArray, socketAck) -> Void in
            completion(dataArray.first as! String)
        }
    }
}
