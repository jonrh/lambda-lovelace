//
//  EvaluationProgressView.swift
//  LovelaceEvaluation
//
//  Created by Junyang ma on 7/6/16.
//  Copyright © 2016 lovelaceTeam. All rights reserved.
//

import UIKit

// this custom view is used to draw prgress circle
@IBDesignable
class EvaluationProgressView: UIView {
    
    var progressLayer:PieSliceLayer!
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        progressLayer = PieSliceLayer(layer: layer)
        progressLayer.endAngle = progressLayer.startAngle
        layer.insertSublayer(progressLayer, below: layer)
        setNeedsDisplay()
    }
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
        progressLayer = PieSliceLayer(layer: layer)
        progressLayer.endAngle = progressLayer.startAngle
        layer.insertSublayer(progressLayer, atIndex: 0)
        setNeedsDisplay()
    }
    
    override func drawRect(rect: CGRect) {
        let results = EvaluationResult.results
        let selectedChoiceCount = results.filter { $0 != nil }.count
        let startAngle = CGFloat(-M_PI_2)
        let center = CGPoint(x: bounds.midX, y: bounds.midY)
        let radius = bounds.width / 2
        let numberOfSegments = AppConstant.tweetContentViewCount
        let angleStep = 2 * CGFloat(M_PI) / CGFloat(numberOfSegments)
        let endAngle = CGFloat(selectedChoiceCount) * angleStep + startAngle
        
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
        
        progressLayer.endAngle = endAngle
        
    }
    
    

}

class PieSliceLayer:CALayer{
    var startAngle: CGFloat = CGFloat(-M_PI_2)
    @NSManaged var endAngle: CGFloat
    let greenColor = UIColor(hue:0.429, saturation:0.590, brightness:0.837, alpha:1)
    
    override init(layer: AnyObject) {
        super.init(layer: layer)
        frame = layer.frame
        setNeedsDisplay()
    }
    
    override init() {
        super.init()
        setNeedsDisplay()
    }
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
    }
    
    func makeAnimationForKey(key: String) -> CABasicAnimation{
        let animation = CABasicAnimation(keyPath: key)
        animation.fromValue = presentationLayer()?.valueForKey(key)
        animation.timingFunction = CAMediaTimingFunction(name: kCAMediaTimingFunctionEaseInEaseOut)
        animation.duration = 0.5
        
        return animation
    }
    
    override func actionForKey(event: String) -> CAAction? {
        if (event == "startAngle" || event == "endAngle"){
            return makeAnimationForKey(event)
        }
        return super.actionForKey(event)
    }
    
    override class func needsDisplayForKey(key: String) -> Bool{
        if key == "startAngle" || key == "endAngle" {
            return true
        }
        else {
            return super.needsDisplayForKey(key)
        }
    }
    
    override func drawInContext(ctx: CGContext) {
        let center = CGPointMake(self.bounds.size.width/2, self.bounds.size.height/2)
        let radius = center.x
        
        CGContextBeginPath(ctx)
        CGContextMoveToPoint(ctx, center.x, center.y)
        
        let p1 = CGPointMake(center.x + radius * cos(self.startAngle), center.y + radius * sin(self.startAngle))
        CGContextAddLineToPoint(ctx, p1.x, p1.y)
        
        CGContextAddArc(ctx, center.x, center.y, radius, self.startAngle, self.endAngle,0)
        CGContextClosePath(ctx)
        
        CGContextSetFillColorWithColor(ctx, greenColor.CGColor)
        CGContextDrawPath(ctx, .Fill)
    }
}
