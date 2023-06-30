from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random
from datetime import timedelta