//
//  HelloWorldViewController.m
//  Ios2HelloWorld
//
//  Created by Victor Zhou on 7/18/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "HelloWorldViewController.h"

@interface HelloWorldViewController ()


@end

@implementation HelloWorldViewController
@synthesize textField;
@synthesize label;
@synthesize userName = _userName;
- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
}

- (void)viewDidUnload
{
    [self setLabel:nil];
    [self setTextField:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation != UIInterfaceOrientationPortraitUpsideDown);
}

- (IBAction)changeGreeting:(id)sender {
    
    self.userName = self.textField.text;
    
    NSString *nameString = self.userName;

    NSString *greeting = [[NSString alloc] initWithFormat:@"hello %@", nameString];
    self.label.text = greeting;
}

@end
