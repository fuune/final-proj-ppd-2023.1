//
//  SocketIOManager.swift
//  ClientMonitor
//
//  Created by Daniel Barbosa on 28/06/23.
//

import Foundation
import SocketIO

class SocketIOManager: NSObject {
    static let sharedInstance = SocketIOManager()
    
    lazy var manager = SocketManager(socketURL: URL(string: "http://localhost:8000")!, config: [.log(true), .compress])
    lazy var socket = manager.defaultSocket

    let username = "admin"

    override init() {
        super.init()
    }
    
    func establishConnection() {
        socket.connect(withPayload: ["username": username])
    }
    
    func closeConnection() {
        socket.disconnect()
    }
    
    func addWatchedWord(word: String) {
        socket.emit("register_watched_word", word)
    }
}
