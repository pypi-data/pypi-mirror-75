    if (c == ' ') {
        do {
            
            NEXTCHAR2_INQUOTES(goodend);
        } while (c == ' ');
    }
    else {
    }
    if ((digit = c ^ '0') <= 9) {
        value = value * 10 + digit;
        NEXTCHAR2_INQUOTES(goodend);
        if ((digit = c ^ '0') <= 9 && (value - 922337203685477580) + ((digit + 8) >> 4) <= 0) {
            do {
                value = value * 10 + digit;
                NEXTCHAR2_INQUOTES(goodend);
            } while ((digit = c ^ '0') <= 9 && (value - 922337203685477580) + ((digit + 8) >> 4) <= 0);
        }
        else {
        }
        if ((digit = c ^ '0') <= 9) {
            do {
                --fracexpo;
                NEXTCHAR2_INQUOTES(goodend);
            } while ((digit = c ^ '0') <= 9);
        }
        else {
        }
        if (c == '.') {
            
            NEXTCHAR2_INQUOTES(goodend);
            if ((digit = c ^ '0') <= 9 && (value - 922337203685477580) + ((digit + 8) >> 4) <= 0) {
                do {
                    value = value * 10 + digit; ++fracexpo;
                    NEXTCHAR2_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9 && (value - 922337203685477580) + ((digit + 8) >> 4) <= 0);
            }
            else {
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR2_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
        }
        else {
        }
        if ((c | 32) == 'e') {
            
            NEXTCHAR2_INQUOTES(badend);
            if (c == '+') {
                
                NEXTCHAR2_INQUOTES(badend);
            }
            else if (c == '-') {
                exposign = -1;
                NEXTCHAR2_INQUOTES(badend);
            }
            else {
            }
            if ((digit = c ^ '0') <= 9) {
                expo = (expo * 10 + digit) & 511;
                NEXTCHAR2_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    expo = (expo * 10 + digit) & 511;
                    NEXTCHAR2_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
        }
        else {
        }
    }
    else if (c == '.') {
        
        NEXTCHAR2_INQUOTES(badend);
        if ((digit = c ^ '0') <= 9) {
            value = value * 10 + digit; ++fracexpo;
            NEXTCHAR2_INQUOTES(goodend);
        }
        else {
            goto bad;
        }
        if ((digit = c ^ '0') <= 9 && (value - 922337203685477580) + ((digit + 8) >> 4) <= 0) {
            do {
                value = value * 10 + digit; ++fracexpo;
                NEXTCHAR2_INQUOTES(goodend);
            } while ((digit = c ^ '0') <= 9 && (value - 922337203685477580) + ((digit + 8) >> 4) <= 0);
        }
        else {
        }
        if ((digit = c ^ '0') <= 9) {
            do {
                
                NEXTCHAR2_INQUOTES(goodend);
            } while ((digit = c ^ '0') <= 9);
        }
        else {
        }
        if ((c | 32) == 'e') {
            
            NEXTCHAR2_INQUOTES(badend);
            if (c == '+') {
                
                NEXTCHAR2_INQUOTES(badend);
            }
            else if (c == '-') {
                exposign = -1;
                NEXTCHAR2_INQUOTES(badend);
            }
            else {
            }
            if ((digit = c ^ '0') <= 9) {
                expo = (expo * 10 + digit) & 511;
                NEXTCHAR2_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    expo = (expo * 10 + digit) & 511;
                    NEXTCHAR2_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
        }
        else {
        }
    }
    else if ((c | 32) == 'i') {
        
        NEXTCHAR2_INQUOTES(badend);
        if ((c | 32) == 'n') {
            
            NEXTCHAR2_INQUOTES(badend);
        }
        else {
            goto bad;
        }
        if ((c | 32) == 'f') {
            expo = INT_MAX; value = 1;
            NEXTCHAR2_INQUOTES(goodend);
        }
        else {
            goto bad;
        }
    }
    else if ((c | 32) == 'n') {
        
        NEXTCHAR2_INQUOTES(badend);
        if ((c | 32) == 'a') {
            
            NEXTCHAR2_INQUOTES(badend);
        }
        else {
            goto bad;
        }
        if ((c | 32) == 'n') {
            expo = INT_MIN;
            NEXTCHAR2_INQUOTES(goodend);
        }
        else {
            goto bad;
        }
    }
    else if (c == '+') {
        
        NEXTCHAR2_INQUOTES(badend);
        if ((digit = c ^ '0') <= 9) {
            value = value * 10 + digit;
            NEXTCHAR2_INQUOTES(goodend);
            if ((digit = c ^ '0') <= 9 && (value - 922337203685477580) + ((digit + 8) >> 4) <= 0) {
                do {
                    value = value * 10 + digit;
                    NEXTCHAR2_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9 && (value - 922337203685477580) + ((digit + 8) >> 4) <= 0);
            }
            else {
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    --fracexpo;
                    NEXTCHAR2_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
            if (c == '.') {
                
                NEXTCHAR2_INQUOTES(goodend);
                if ((digit = c ^ '0') <= 9 && (value - 922337203685477580) + ((digit + 8) >> 4) <= 0) {
                    do {
                        value = value * 10 + digit; ++fracexpo;
                        NEXTCHAR2_INQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9 && (value - 922337203685477580) + ((digit + 8) >> 4) <= 0);
                }
                else {
                }
                if ((digit = c ^ '0') <= 9) {
                    do {
                        
                        NEXTCHAR2_INQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
            if ((c | 32) == 'e') {
                
                NEXTCHAR2_INQUOTES(badend);
                if (c == '+') {
                    
                    NEXTCHAR2_INQUOTES(badend);
                }
                else if (c == '-') {
                    exposign = -1;
                    NEXTCHAR2_INQUOTES(badend);
                }
                else {
                }
                if ((digit = c ^ '0') <= 9) {
                    expo = (expo * 10 + digit) & 511;
                    NEXTCHAR2_INQUOTES(goodend);
                }
                else {
                    goto bad;
                }
                if ((digit = c ^ '0') <= 9) {
                    do {
                        expo = (expo * 10 + digit) & 511;
                        NEXTCHAR2_INQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
        }
        else if (c == '.') {
            
            NEXTCHAR2_INQUOTES(badend);
            if ((digit = c ^ '0') <= 9) {
                value = value * 10 + digit; ++fracexpo;
                NEXTCHAR2_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
            if ((digit = c ^ '0') <= 9 && (value - 922337203685477580) + ((digit + 8) >> 4) <= 0) {
                do {
                    value = value * 10 + digit; ++fracexpo;
                    NEXTCHAR2_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9 && (value - 922337203685477580) + ((digit + 8) >> 4) <= 0);
            }
            else {
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR2_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
            if ((c | 32) == 'e') {
                
                NEXTCHAR2_INQUOTES(badend);
                if (c == '+') {
                    
                    NEXTCHAR2_INQUOTES(badend);
                }
                else if (c == '-') {
                    exposign = -1;
                    NEXTCHAR2_INQUOTES(badend);
                }
                else {
                }
                if ((digit = c ^ '0') <= 9) {
                    expo = (expo * 10 + digit) & 511;
                    NEXTCHAR2_INQUOTES(goodend);
                }
                else {
                    goto bad;
                }
                if ((digit = c ^ '0') <= 9) {
                    do {
                        expo = (expo * 10 + digit) & 511;
                        NEXTCHAR2_INQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
        }
        else if ((c | 32) == 'i') {
            
            NEXTCHAR2_INQUOTES(badend);
            if ((c | 32) == 'n') {
                
                NEXTCHAR2_INQUOTES(badend);
            }
            else {
                goto bad;
            }
            if ((c | 32) == 'f') {
                expo = INT_MAX; value = 1;
                NEXTCHAR2_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
        }
        else if ((c | 32) == 'n') {
            
            NEXTCHAR2_INQUOTES(badend);
            if ((c | 32) == 'a') {
                
                NEXTCHAR2_INQUOTES(badend);
            }
            else {
                goto bad;
            }
            if ((c | 32) == 'n') {
                expo = INT_MIN;
                NEXTCHAR2_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
        }
        else {
            goto bad;
        }
    }
    else if (c == '-') {
        
        NEXTCHAR2_INQUOTES(badend);
        if ((digit = c ^ '0') <= 9) {
            value = value * 10 - digit;
            NEXTCHAR2_INQUOTES(goodend);
            if ((digit = c ^ '0') <= 9 && (-value - 922337203685477580) + ((digit + 7) >> 4) <= 0) {
                do {
                    value = value * 10 - digit;
                    NEXTCHAR2_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9 && (-value - 922337203685477580) + ((digit + 7) >> 4) <= 0);
            }
            else {
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    --fracexpo;
                    NEXTCHAR2_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
            if (c == '.') {
                
                NEXTCHAR2_INQUOTES(goodend);
                if ((digit = c ^ '0') <= 9 && (-value - 922337203685477580) + ((digit + 7) >> 4) <= 0) {
                    do {
                        value = value * 10 - digit; ++fracexpo;
                        NEXTCHAR2_INQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9 && (-value - 922337203685477580) + ((digit + 7) >> 4) <= 0);
                }
                else {
                }
                if ((digit = c ^ '0') <= 9) {
                    do {
                        
                        NEXTCHAR2_INQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
            if ((c | 32) == 'e') {
                
                NEXTCHAR2_INQUOTES(badend);
                if (c == '+') {
                    
                    NEXTCHAR2_INQUOTES(badend);
                }
                else if (c == '-') {
                    exposign = -1;
                    NEXTCHAR2_INQUOTES(badend);
                }
                else {
                }
                if ((digit = c ^ '0') <= 9) {
                    expo = (expo * 10 + digit) & 511;
                    NEXTCHAR2_INQUOTES(goodend);
                }
                else {
                    goto bad;
                }
                if ((digit = c ^ '0') <= 9) {
                    do {
                        expo = (expo * 10 + digit) & 511;
                        NEXTCHAR2_INQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
        }
        else if (c == '.') {
            
            NEXTCHAR2_INQUOTES(badend);
            if ((digit = c ^ '0') <= 9) {
                value = value * 10 - digit; ++fracexpo;
                NEXTCHAR2_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
            if ((digit = c ^ '0') <= 9 && (-value - 922337203685477580) + ((digit + 7) >> 4) <= 0) {
                do {
                    value = value * 10 - digit; ++fracexpo;
                    NEXTCHAR2_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9 && (-value - 922337203685477580) + ((digit + 7) >> 4) <= 0);
            }
            else {
            }
            if ((digit = c ^ '0') <= 9) {
                do {
                    
                    NEXTCHAR2_INQUOTES(goodend);
                } while ((digit = c ^ '0') <= 9);
            }
            else {
            }
            if ((c | 32) == 'e') {
                
                NEXTCHAR2_INQUOTES(badend);
                if (c == '+') {
                    
                    NEXTCHAR2_INQUOTES(badend);
                }
                else if (c == '-') {
                    exposign = -1;
                    NEXTCHAR2_INQUOTES(badend);
                }
                else {
                }
                if ((digit = c ^ '0') <= 9) {
                    expo = (expo * 10 + digit) & 511;
                    NEXTCHAR2_INQUOTES(goodend);
                }
                else {
                    goto bad;
                }
                if ((digit = c ^ '0') <= 9) {
                    do {
                        expo = (expo * 10 + digit) & 511;
                        NEXTCHAR2_INQUOTES(goodend);
                    } while ((digit = c ^ '0') <= 9);
                }
                else {
                }
            }
            else {
            }
        }
        else if ((c | 32) == 'i') {
            
            NEXTCHAR2_INQUOTES(badend);
            if ((c | 32) == 'n') {
                
                NEXTCHAR2_INQUOTES(badend);
            }
            else {
                goto bad;
            }
            if ((c | 32) == 'f') {
                expo = INT_MAX; value = -1;
                NEXTCHAR2_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
        }
        else if ((c | 32) == 'n') {
            
            NEXTCHAR2_INQUOTES(badend);
            if ((c | 32) == 'a') {
                
                NEXTCHAR2_INQUOTES(badend);
            }
            else {
                goto bad;
            }
            if ((c | 32) == 'n') {
                expo = INT_MIN;
                NEXTCHAR2_INQUOTES(goodend);
            }
            else {
                goto bad;
            }
        }
        else {
            goto bad;
        }
    }
    else {
    }
    if (c == ' ') {
        do {
            
            NEXTCHAR2_INQUOTES(goodend);
        } while (c == ' ');
    }
    else {
    }
