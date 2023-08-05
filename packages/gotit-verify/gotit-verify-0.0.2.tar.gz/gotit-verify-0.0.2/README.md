# GotIt Verify SDK

## Description
This SDK is used to verify the identity of an app that 
attempts to access Got It APIs. The client of the app
needs to provide an environment name, app key an app secret
to use the SDK.

## Installation 


## Usage

    from gotit_verify import Verify
    verify = Verify(env, app_key, app_secret)

    new_auth = verify.create_verification(
                            channel, template_name, to, 
                            subject_params={}, body_params = {}
                            )

    check_auth = verify.check_verification(channel, to, code)

The two respective variables will contain the content as followed:

    check_auth: Dict{
                    id:int, 
                    channel: str, 
                    to: str, 
                    code: str, 
                    status: str, 
                    denied_reasons: str
                   }
    
    new_auth: Dict{ 
                    id: int,
                    channel: str,
                    template_name: str,
                    subject_params: dict,
                    body_params: dict,
                    code: str,
                    expiration_date: str,
                    status: str 
                  }

## LICENSE