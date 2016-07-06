//
//  EvaluationProgressView.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 7/6/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

@IBDesignable
class EvaluationProgressView: UIView {
    
    var currentPageNumber = 0

    // Only override drawRect: if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    let numberOfSegments = AppConstant.tweetContentViewCount
    override func drawRect(rect: CGRect) {
        // Drawing code
        let center = CGPoint(x: bounds.midX, y: bounds.midY)
        let radius = bounds.width / 2
        let angleStep = 2 * CGFloat(M_PI) / CGFloat(numberOfSegments)
        let startAngle = CGFloat(-M_PI_2)
        let endAngle = CGFloat(currentPageNumber + 1) * angleStep + startAngle
        
        var path = UIBezierPath()
        
        for i in 0..<numberOfSegments{
            path = UIBezierPath()
            let angle = startAngle + CGFloat(i) * angleStep
            let x = radius * cos(angle) + center.x
            let y = radius * sin(angle) + center.y
            let point = CGPoint(x: x, y: y)
            path.moveToPoint(point)
            path.addLineToPoint(center)
            let darkLineColor = UIColor(hue:0.567, saturation:0.326, brightness:0.45, alpha:1)
            darkLineColor.setStroke()
            path.stroke()
        }
        
        path = UIBezierPath(arcCenter: center, radius: radius, startAngle: startAngle, endAngle: endAngle, clockwise: true)
        path.addLineToPoint(center)
        path.closePath()
        let greenColor = UIColor(hue: 0.425, saturation: 0.5, brightness: 1, alpha: 1.0) /* #7dffc6 */
        greenColor.setFill()
        path.fill()
        
        
        let shadowView = UIImage(named: "progress shadow")
        let numberBaseView = UIImage(named: "progress white")
        shadowView?.drawInRect(bounds)
        let numberBaseRect = CGRect(x: 11, y: 11, width: 42, height: 42)
        numberBaseView?.drawInRect(numberBaseRect)
    }
    

}
