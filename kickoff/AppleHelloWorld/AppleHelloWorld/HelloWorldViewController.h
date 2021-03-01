//
//  HelloWorldViewController.h
//  AppleHelloWorld
//
//  Created by Victor Zhou on 7/24/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface HelloWorldViewController : UIViewController

@property (weak, nonatomic) IBOutlet UITextField *textField;
@property (weak, nonatomic) IBOutlet UILabel *label;
@property (copy, nonatomic) NSString *userName;
- (IBAction)changeGreeting:(id)sender;
    
@end