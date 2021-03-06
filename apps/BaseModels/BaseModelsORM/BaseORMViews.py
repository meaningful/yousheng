#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---------------------------------------------
    File  Name : BaseORMViews
    Author : agony
    Date : 2018/7/29
    Description: 基础数据的ORM models
---------------------------------------------
"""
import datetime
import json
from sqlalchemy import Column, String, Integer, Date, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from dateutil import rrule
from dateutil.relativedelta import relativedelta

# 创建ORM对象的基类
Base = declarative_base()

# 初始化数据库连接:
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
engine = create_engine('mysql+pymysql://root:WLW2017test@47.93.228.118:3306/yousheng')

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


# Datetime 类型json序列化
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


# Python类转dict
def object2dict(obj):
    # convert object to a dict
    d = {}
    # d['__class__'] = obj.__class__.__name__
    # d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    if '_sa_instance_state' in d:
        del d['_sa_instance_state']
    return d


# def dict2object(d):
#     # convert dict to object
#     if '__class__' in d:
#         class_name = d.pop('__class__')
#         module_name = d.pop('__module__')
#         module = __import__(module_name)
#         class_ = getattr(module, class_name)
#         args = dict((key.encode('ascii'), value) for key, value in d.items())  # get args
#         inst = class_(**args)  # create new instance
#     else:
#         inst = d
#     return inst


# <- 客户管理表 Begin ->
# 客户编号		customID
# 名称	单位名称+简称	customName
# 电话		tel
# 地址		addr
# 税号		taxFileNO
# 开户行		bankOfDepsit
# 账号		bankAccount
# 传真		fax
# 所属行业		industryField
# 公司性质		companyNature
# 用气种类	【废弃，不用】	gasCategory
# 储罐大小	【废弃，不用】	gasTankSize
# 合作类型	【直供， 共建，中间站】	consocationMode
# 等级	【A/B/C/D】	level
# 合同	【varchar(256)】 合同号	contract
# 付款周期		payCycle
# 公司负责人		companyCharge
# 公司联系人		companyContact
# 客户资质	三证	customQualification
# 年销售额		annualSales


class CustomerManage(Base):
    __tablename__ = 'BaseModels_customermanage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customID = Column(String(128))
    customName = Column(String(128))
    tel = Column(String(128))
    addr = Column(String(128))
    taxFileNO = Column(String(128))
    bankOfDepsit = Column(String(128))
    bankAccount = Column(String(128))
    fax = Column(String(128))
    industryField = Column(String(128))
    companyNature = Column(String(128))
    consocationMode = Column(String(128))
    level = Column(String(128))
    contract = Column(String(128))
    payCycle = Column(Date)
    companyCharge = Column(String(128))
    companyContact = Column(String(128))
    customQualification = Column(String(128))
    annualSales = Column(String(128))


class CustomerManageDBUtils(object):
    @classmethod
    def add(cls, customer):
        if not isinstance(customer, CustomerManage):
            raise TypeError('The parameter customer is not instance of the CustomerManage instance')
        session = DBSession()
        session.add(customer)
        session.flush()
        new_item_id = customer.id
        session.commit()
        session.close()
        return new_item_id

    @classmethod
    def delete(cls, delId):
        session = DBSession()
        item_to_del = session.query(CustomerManage).filter_by(id=delId).first()
        session.delete(item_to_del)
        session.commit()
        session.close()

    @classmethod
    def update(cls, updateId, customer):
        if not isinstance(customer, CustomerManage):
            raise TypeError('The parameter customer is not instance of the CustomerManage instance')
        session = DBSession()
        item_to_update = session.query(CustomerManage).filter_by(id=updateId).first()
        item_to_update.customID = customer.customID
        item_to_update.customName = customer.customName
        item_to_update.tel = customer.tel
        item_to_update.addr = customer.addr
        item_to_update.taxFileNO = customer.taxFileNO
        item_to_update.bankOfDepsit = customer.bankOfDepsit
        item_to_update.bankAccount = customer.bankAccount
        item_to_update.fax = customer.fax
        item_to_update.industryField = customer.industryField
        item_to_update.companyNature = customer.companyNature
        # item_to_update.gasCategory = customer.gasCategory
        item_to_update.consocationMode = customer.consocationMode
        item_to_update.level = customer.level
        item_to_update.contract = customer.contract
        item_to_update.payCycle = customer.payCycle
        item_to_update.companyCharge = customer.companyCharge
        item_to_update.companyContact = customer.companyContact
        item_to_update.customQualification = customer.customQualification
        item_to_update.annualSales = customer.annualSales

        session.commit()
        session.close()

    @classmethod
    def queryAll(cls):
        session = DBSession()
        queryAll = session.query(CustomerManage).all()
        allCustomer = []
        for item in queryAll:
            customer_json = json.dumps(object2dict(item), cls=DateEncoder)
            customer = json.loads(customer_json)
            allCustomer.append(customer)
        session.close()
        return allCustomer

    @classmethod
    def queryByCustomName(cls, customName):
        session = DBSession()
        queryItem = session.query(CustomerManage).filter(CustomerManage.customName == customName).first()
        customer_json = json.dumps(object2dict(queryItem), cls=DateEncoder)
        customer = json.loads(customer_json)
        session.close()
        return customer


# <- 客户管理表 End ->

# <- 供货商管理表 Begin ->
# 供应商编号		supplierID
# 单位名称		supplierName
# 电话		tel
# 地址		addr
# 公司负责人（姓名）		companyChargeName
# 公司负责人（职务）		companyChargePosition
# 公司负责人（电话）		companyChargeTel
# 公司联系人（姓名）		companyContactName
# 公司联系人（职务）		companyContactPosition
# 公司联系人（电话）		companyContactTel
# 客户资质	三证	customQualification
# 客户资质（税号）		customTaxFileNO
# 客户资质（开户行）		customBankOfDepsit
# 客户资质（账号）		customBankAccount
# 客户资质（联系人）		customContactName
# 客户资质（手机）		customContactTel
# 采购品种		purchaseCategory

class Supplier(Base):
    __tablename__ = 'BaseModels_supplier'

    id = Column(Integer, primary_key=True, autoincrement=True)
    supplierID = Column(String(128))
    supplierName = Column(String(128))
    tel = Column(String(128))
    addr = Column(String(128))
    companyChargeName = Column(String(128))
    companyChargePosition = Column(String(128))
    companyChargeTel = Column(String(128))
    companyContactName = Column(String(128))
    companyContactPosition = Column(String(128))
    companyContactTel = Column(String(128))
    customQualification = Column(String(128))
    customTaxFileNO = Column(String(128))
    customBankOfDepsit = Column(String(128))
    customBankAccount = Column(String(128))
    customContactName = Column(String(128))
    customContactTel = Column(String(128))
    purchaseCategory = Column(String(128))


class SupplierDBUtils(object):
    @classmethod
    def add(cls, supplier):
        if not isinstance(supplier, Supplier):
            raise TypeError('The parameter supplier is not instance of the Supplier instance')
        session = DBSession()
        session.add(supplier)
        session.flush()
        new_item_id = supplier.id
        session.commit()
        session.close()
        return new_item_id

    @classmethod
    def delete(cls, delId):
        session = DBSession()
        item_to_del = session.query(Supplier).filter_by(id=delId).first()
        session.delete(item_to_del)
        session.commit()
        session.close()

    @classmethod
    def update(cls, updateId, supplier):
        if not isinstance(supplier, Supplier):
            raise TypeError('The parameter supplier  is not instance of the Supplier instance')
        session = DBSession()
        item_to_update = session.query(Supplier).filter_by(id=updateId).first()
        item_to_update.supplierID = supplier.supplierID
        item_to_update.supplierName = supplier.supplierName
        item_to_update.tel = supplier.tel
        item_to_update.addr = supplier.addr
        item_to_update.companyChargeName = supplier.companyChargeName
        item_to_update.companyChargePosition = supplier.companyChargePosition
        item_to_update.companyChargeTel = supplier.companyChargeTel
        item_to_update.companyContactName = supplier.companyContactName
        item_to_update.companyContactPosition = supplier.companyContactPosition
        item_to_update.companyContactTel = supplier.companyContactTel
        item_to_update.customQualification = supplier.customQualification
        item_to_update.customTaxFileNO = supplier.customTaxFileNO
        item_to_update.customBankOfDepsit = supplier.customBankOfDepsit
        item_to_update.customBankAccount = supplier.customBankAccount
        item_to_update.customContactName = supplier.customContactName
        item_to_update.customContactTel = supplier.customContactTel
        item_to_update.purchaseCategory = supplier.purchaseCategory
        session.commit()
        session.close()

    @classmethod
    def queryAll(cls):
        session = DBSession()
        queryAll = session.query(Supplier).all()
        allSuppliers = []
        for item in queryAll:
            supplier_json = json.dumps(object2dict(item), cls=DateEncoder)
            supplier = json.loads(supplier_json)
            allSuppliers.append(supplier)
        session.close()
        return allSuppliers

# <- 供货商管理表 End ->

# <- 公司人员管理表 Begin ->
# 编号		staffID
# 姓名		staffName
# 身份证号		idNumber
# 入职时间		hiredate
# 职务		position
# 照片		photo
# 人员简历		resume
# 人员类别	（办公室/司机/押运员）	category


class StaffManage(Base):
    __tablename__ = 'BaseModels_staffmanage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    staffID = Column(String(128))
    staffName = Column(String(128))
    idNumber = Column(String(128))
    hiredate = Column(Date)
    position = Column(String(128))
    photo = Column(String(128))
    resume = Column(String(128))
    category = Column(String(128))


# StaffManage 数据库操作类
class StaffManageDBUtils(object):
    STAFF_CATEGORY_DRIVER = "司机"
    STAFF_CATEGORY_SUPERCARGO = "押运员"

    @classmethod
    def add(cls, staff):
        if not isinstance(staff, StaffManage):
            raise TypeError('The parameter staff is not instance of the StaffManage instance')
        session = DBSession()
        session.add(staff)
        session.flush()
        new_item_id = staff.id
        session.commit()
        session.close()
        return new_item_id

    @classmethod
    def delete(cls, delId):
        session = DBSession()
        item_to_del = session.query(StaffManage).filter_by(id=delId).first()
        session.delete(item_to_del)
        session.commit()
        session.close()

    @classmethod
    def update(cls, updateId, staff):
        if not isinstance(staff, StaffManage):
            raise TypeError('The parameter staff is not instance of the StaffManage instance')
        session = DBSession()
        item_to_update = session.query(StaffManage).filter_by(id=updateId).first()
        item_to_update.staffID = staff.staffID
        item_to_update.staffName = staff.staffName
        item_to_update.idNumber = staff.idNumber
        item_to_update.hiredate = staff.hiredate
        item_to_update.position = staff.position
        item_to_update.photo = staff.photo
        item_to_update.resume = staff.resume
        item_to_update.category = staff.category
        session.commit()
        session.close()

    @classmethod
    def queryAll(cls):
        session = DBSession()
        queryAll = session.query(StaffManage).all()
        allStaffs = []
        for item in queryAll:
            staff_json = json.dumps(object2dict(item), cls=DateEncoder)
            staff = json.loads(staff_json)
            allStaffs.append(staff)
        session.close()
        return allStaffs

    # 根据人员category查询
    @classmethod
    def queryAllByCategory(cls, category):
        session = DBSession()
        queryAllByCategory = session.query(StaffManage).filter(StaffManage.category == category).all()
        allStaffCatagory = []
        for item in queryAllByCategory:
            staff_json = json.dumps(object2dict(item), cls=DateEncoder)
            staff = json.loads(staff_json)
            allStaffCatagory.append(staff)
            session.close()
        return allStaffCatagory


# <- 公司人员管理表 End ->


# <- 气体管理表 Begin ->
# 气体编号		gasID
# 气体名称		gasName


class GasManage(Base):
    __tablename__ = 'BaseModels_gasmanage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gasID = Column(String(128))
    gasName = Column(String(128))


class GasManageDBUtils(object):
    @classmethod
    def add(cls, gas):
        if not isinstance(gas, GasManage):
            raise TypeError('The parameter gas is not instance of the GasManage instance')
        session = DBSession()
        session.add(gas)
        session.flush()
        new_item_id = gas.id
        session.commit()
        session.close()
        return new_item_id

    @classmethod
    def delete(cls, delId):
        session = DBSession()
        item_to_del = session.query(GasManage).filter_by(id=delId).first()
        session.delete(item_to_del)
        session.commit()
        session.close()

    @classmethod
    def update(cls, updateId, gas):
        if not isinstance(gas, GasManage):
            raise TypeError('The parameter gas is not instance of the GasManage instance')
        session = DBSession()
        item_to_update = session.query(GasManage).filter_by(id=updateId).first()
        item_to_update.gasID = gas.gasID
        item_to_update.gasName = gas.gasName
        session.commit()
        session.close()

    @classmethod
    def queryAll(cls):
        session = DBSession()
        queryAll = session.query(GasManage).all()
        allGas = []
        for item in queryAll:
            gas_json = json.dumps(object2dict(item), cls=DateEncoder)
            gas = json.loads(gas_json)
            allGas.append(gas)
        session.close()
        return allGas


# <- 气体管理表 End ->

# <- 拖车管理表 Begin ->
# 车牌号		tractorID
# 年检时间		annualInspectionTime
# 年检周期       annualInspectionCycle
# 保险时间		insuranceTime
# 车架号		chassisNumber
# 出厂时间		deliveryTime
# 初始码表数    initMileage


class TractorManage(Base):
    __tablename__ = 'BaseModels_tractormanage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tractorID = Column(String(128))
    annualInspectionTime = Column(Date)
    annualInspectionCycle = Column(Integer)
    insuranceTime = Column(Date)
    chassisNumber = Column(String(128))
    deliveryTime = Column(String(128))
    initMileage = Column(String(128))


class TractorManageDBUtils(object):
    @classmethod
    def add(cls, tractor):
        if not isinstance(tractor, TractorManage):
            raise TypeError('The parameter tractor is not instance of the TractorManage instance')
        session = DBSession()
        session.add(tractor)
        session.flush()
        new_item_id = tractor.id
        session.commit()
        session.close()
        return new_item_id

    @classmethod
    def delete(cls, delId):
        session = DBSession()
        item_to_del = session.query(TractorManage).filter_by(id=delId).first()
        session.delete(item_to_del)
        session.commit()
        session.close()

    @classmethod
    def update(cls, updateId, tractor):
        if not isinstance(tractor, TractorManage):
            raise TypeError('The parameter tractor is not instance of the TractorManage instance')
        session = DBSession()
        item_to_update = session.query(TractorManage).filter_by(id=updateId).first()
        item_to_update.tractorID = tractor.tractorID
        item_to_update.annualInspectionTime = tractor.annualInspectionTime
        item_to_update.annualInspectionCycle = tractor.annualInspectionCycle
        item_to_update.insuranceTime = tractor.insuranceTime
        item_to_update.chassisNumber = tractor.chassisNumber
        item_to_update.deliveryTime = tractor.deliveryTime
        session.commit()
        session.close()

    @classmethod
    def updateBytractorID(cls, tractor):
        if not isinstance(tractor, TractorManage):
            raise TypeError('The parameter tractor is not instance of the TractorManage instance')
        session = DBSession()
        item_to_update = session.query(TractorManage).filter(TractorManage.tractorID == tractor.tractorID).first()
        item_to_update.tractorID = tractor.tractorID
        item_to_update.annualInspectionTime = tractor.annualInspectionTime
        item_to_update.annualInspectionCycle = tractor.annualInspectionCycle
        item_to_update.insuranceTime = tractor.insuranceTime
        item_to_update.chassisNumber = tractor.chassisNumber
        item_to_update.deliveryTime = tractor.deliveryTime
        session.commit()
        session.close()

    @classmethod
    def queryAll(cls):
        session = DBSession()
        queryAll = session.query(TractorManage).all()
        allTractor = []
        for item in queryAll:
            tractor_json = json.dumps(object2dict(item), cls=DateEncoder)
            tractor = json.loads(tractor_json)
            allTractor.append(tractor)
        session.close()
        return allTractor


# <- 拖车管理表 End ->


# <- 挂车管理表 Begin ->
# 挂车号		trailerID
# 年检时间		annualInspectionTime
# 年检周期       annualInspectionCycle
# 保险时间		insuranceTime
# 车架号		chassisNumber
# 出厂时间		deliveryTime


class TrailerManage(Base):
    __tablename__ = 'BaseModels_trailermanage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    trailerID = Column(String(128))
    annualInspectionTime = Column(Date)
    annualInspectionCycle = Column(Integer)
    insuranceTime = Column(Date)
    chassisNumber = Column(String(128))
    deliveryTime = Column(String(128))
    currentBalance = Column(String(128))


class TrailerManageDBUtils(object):
    @classmethod
    def add(cls, trailer):
        if not isinstance(trailer, TrailerManage):
            raise TypeError('The parameter trailer is not instance of the TrailerManage instance')
        session = DBSession()
        session.add(trailer)
        session.flush()
        new_item_id = trailer.id
        session.commit()
        session.close()
        return new_item_id

    @classmethod
    def delete(cls, delId):
        session = DBSession()
        item_to_del = session.query(TrailerManage).filter_by(id=delId).first()
        session.delete(item_to_del)
        session.commit()
        session.close()

    @classmethod
    def update(cls, updateId, trailer):
        if not isinstance(trailer, TrailerManage):
            raise TypeError('The parameter tractor is not instance of the TractorManage instance')
        session = DBSession()
        item_to_update = session.query(TrailerManage).filter_by(id=updateId).first()
        item_to_update.trailerID = trailer.trailerID
        item_to_update.annualInspectionTime = trailer.annualInspectionTime
        item_to_update.annualInspectionCycle = trailer.annualInspectionCycle
        item_to_update.insuranceTime = trailer.insuranceTime
        item_to_update.chassisNumber = trailer.chassisNumber
        item_to_update.deliveryTime = trailer.deliveryTime
        item_to_update.currentBalance = trailer.currentBalance
        session.commit()
        session.close()

    @classmethod
    def updateBytrailerID(cls, trailer):
        if not isinstance(trailer, TrailerManage):
            raise TypeError('The parameter trailer is not instance of the TrailerManage instance')
        session = DBSession()
        item_to_update = session.query(TrailerManage).filter(TrailerManage.trailerID == trailer.trailerID).first()
        item_to_update.trailerID = trailer.trailerID
        item_to_update.annualInspectionTime = trailer.annualInspectionTime
        item_to_update.annualInspectionCycle = trailer.annualInspectionCycle
        item_to_update.insuranceTime = trailer.insuranceTime
        item_to_update.chassisNumber = trailer.chassisNumber
        item_to_update.deliveryTime = trailer.deliveryTime
        session.commit()
        session.close()

    @classmethod
    def queryAll(cls):
        session = DBSession()
        queryAll = session.query(TrailerManage).all()
        allTrailer = []
        for item in queryAll:
            trailer_json = json.dumps(object2dict(item), cls=DateEncoder)
            trailer = json.loads(trailer_json)
            allTrailer.append(trailer)
        session.close()
        return allTrailer


# <- 挂车管理表 End ->


# <- 用户管理表 Begin ->
# 用户名		userName
# 密码		userPassword
# 用户权限级别 userLevel


class User(Base):
    __tablename__ = 'Yousheng_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String(128))
    userPassword = Column(String(256))
    userLevel = Column(String(128))


class UserDBUtils(object):
    @classmethod
    def add(cls, user):
        if not isinstance(user, User):
            raise TypeError('The parameter user is not instance of the User instance')
        session = DBSession()
        session.add(user)
        session.flush()
        new_item_id = user.id
        session.commit()
        session.close()
        return new_item_id

    @classmethod
    def delete(cls, delId):
        session = DBSession()
        item_to_del = session.query(User).filter_by(id=delId).first()
        session.delete(item_to_del)
        session.commit()
        session.close()

    @classmethod
    def update(cls, updateId, user):
        if not isinstance(user, User):
            raise TypeError('The parameter user is not instance of the User instance')
        session = DBSession()
        item_to_update = session.query(User).filter_by(id=updateId).first()
        item_to_update.userName = user.userName
        item_to_update.userPassword = user.userPassword
        item_to_update.userLevel = user.userLevel
        session.commit()
        session.close()

    @classmethod
    def queryAll(cls):
        session = DBSession()
        queryAll = session.query(User).all()
        allUsers = []
        for item in queryAll:
            user_json = json.dumps(object2dict(item), cls=DateEncoder)
            user = json.loads(user_json)
            allUsers.append(user)
        session.close()
        return allUsers

    @classmethod
    def isUserExist(cls, name, password):
        session = DBSession()
        user = session.query(User).filter(User.userName == name, User.userPassword == password).one_or_none()
        session.close()
        if user:
            return user
        else:
            return None


# <- 用户管理表 end ->


# vehicleType  车辆类型（挂车/拖车）
# vehicleID    车辆编号
# lastAnnualInspectionTime 上次年检时间
# annualInspectionCycle  年检周期
# nextAnnualInspectionTime 下次年检时间
# intervalDeadline  距离下次年检天数

class VehicleMaintenanceTip(object):

    def __init__(self, vehicleType, vehicleID, lastAnnualInspectionTime, annualInspectionCycle,
                 nextAnnualInspectionTime, intervalDeadline):
        self.vehicleType = vehicleType
        self.vehicleID = vehicleID
        self.lastAnnualInspectionTime = lastAnnualInspectionTime
        self.annualInspectionCycle = annualInspectionCycle
        self.nextAnnualInspectionTime = nextAnnualInspectionTime
        self.intervalDeadline = intervalDeadline


class BaseViewUtils(object):

    @classmethod
    def getSelectDataForSaleListReport(cls):
        session = DBSession()
        queryAllCustom = session.query(CustomerManage).all()
        allCustomer = []
        for item in queryAllCustom:
            customer_json = json.dumps(object2dict(item), cls=DateEncoder)
            customer = json.loads(customer_json)
            allCustomer.append(customer)

        queryAllGas = session.query(GasManage).all()
        allGas = []
        for item in queryAllGas:
            gas_json = json.dumps(object2dict(item), cls=DateEncoder)
            gas = json.loads(gas_json)
            allGas.append(gas)

        session.close()

        return {"allCustomer": allCustomer,
                "allGas": allGas}

    @classmethod
    def getSelectDataForMaterialPurchaseReport(cls):
        session = DBSession()

        queryAllSuppliers = session.query(Supplier).all()
        allSuppliers = []
        for item in queryAllSuppliers:
            supplier_json = json.dumps(object2dict(item), cls=DateEncoder)
            supplier = json.loads(supplier_json)
            allSuppliers.append(supplier)

        queryAllGas = session.query(GasManage).all()
        allGas = []
        for item in queryAllGas:
            gas_json = json.dumps(object2dict(item), cls=DateEncoder)
            gas = json.loads(gas_json)
            allGas.append(gas)

        session.close()

        return {"allSuppliers": allSuppliers,
                "allGas": allGas}

    # 查询销售单 Select item 的数据
    @classmethod
    def getAllSelectItemDataForSaleList(cls):

        session = DBSession()

        queryAllCustom = session.query(CustomerManage).all()
        allCustomer = []
        for item in queryAllCustom:
            customer_json = json.dumps(object2dict(item), cls=DateEncoder)
            customer = json.loads(customer_json)
            allCustomer.append(customer)

        queryAllGas = session.query(GasManage).all()
        allGas = []
        for item in queryAllGas:
            gas_json = json.dumps(object2dict(item), cls=DateEncoder)
            gas = json.loads(gas_json)
            allGas.append(gas)

        queryAllTractor = session.query(TractorManage).all()
        allTractor = []
        for item in queryAllTractor:
            tractor_json = json.dumps(object2dict(item), cls=DateEncoder)
            tractor = json.loads(tractor_json)
            allTractor.append(tractor)

        queryAllTrailer = session.query(TrailerManage).all()
        allTrailer = []
        for item in queryAllTrailer:
            trailer_json = json.dumps(object2dict(item), cls=DateEncoder)
            trailer = json.loads(trailer_json)
            allTrailer.append(trailer)

        queryAllDrivers = session.query(StaffManage).filter(
            StaffManage.category == StaffManageDBUtils.STAFF_CATEGORY_DRIVER).all()
        allDrivers = []
        for item in queryAllDrivers:
            driver_json = json.dumps(object2dict(item), cls=DateEncoder)
            driver = json.loads(driver_json)
            allDrivers.append(driver)

        queryAllSupercargo = session.query(StaffManage).filter(
            StaffManage.category == StaffManageDBUtils.STAFF_CATEGORY_SUPERCARGO).all()
        allSupercargo = []
        for item in queryAllSupercargo:
            supercargo_json = json.dumps(object2dict(item), cls=DateEncoder)
            supercargo = json.loads(supercargo_json)
            allSupercargo.append(supercargo)

        session.close()

        return {"allCustomer": allCustomer,
                "allGas": allGas,
                "allTractor": allTractor,
                "allTrailer": allTrailer,
                "allDrivers": allDrivers,
                "allSupercargo": allSupercargo
                }

    # 查询采购单 Select item 的数据
    @classmethod
    def getAllSelectItemDataForMaterialPurchase(cls):

        session = DBSession()

        queryAllSuppliers = session.query(Supplier).all()
        allSuppliers = []
        for item in queryAllSuppliers:
            supplier_json = json.dumps(object2dict(item), cls=DateEncoder)
            supplier = json.loads(supplier_json)
            allSuppliers.append(supplier)

        queryAllGas = session.query(GasManage).all()
        allGas = []
        for item in queryAllGas:
            gas_json = json.dumps(object2dict(item), cls=DateEncoder)
            gas = json.loads(gas_json)
            allGas.append(gas)

        queryAllTractor = session.query(TractorManage).all()
        allTractor = []
        for item in queryAllTractor:
            tractor_json = json.dumps(object2dict(item), cls=DateEncoder)
            tractor = json.loads(tractor_json)
            allTractor.append(tractor)

        queryAllTrailer = session.query(TrailerManage).all()
        allTrailer = []
        for item in queryAllTrailer:
            trailer_json = json.dumps(object2dict(item), cls=DateEncoder)
            trailer = json.loads(trailer_json)
            allTrailer.append(trailer)

        queryAllDrivers = session.query(StaffManage).filter(
            StaffManage.category == StaffManageDBUtils.STAFF_CATEGORY_DRIVER).all()
        allDrivers = []
        for item in queryAllDrivers:
            driver_json = json.dumps(object2dict(item), cls=DateEncoder)
            driver = json.loads(driver_json)
            allDrivers.append(driver)

        queryAllSupercargo = session.query(StaffManage).filter(
            StaffManage.category == StaffManageDBUtils.STAFF_CATEGORY_SUPERCARGO).all()
        allSupercargo = []
        for item in queryAllSupercargo:
            supercargo_json = json.dumps(object2dict(item), cls=DateEncoder)
            supercargo = json.loads(supercargo_json)
            allSupercargo.append(supercargo)

        session.close()

        return {"allSuppliers": allSuppliers,
                "allGas": allGas,
                "allTractor": allTractor,
                "allTrailer": allTrailer,
                "allDrivers": allDrivers,
                "allSupercargo": allSupercargo
                }

    # Home page 基础信息查询
    @classmethod
    def getBaseInfoForHome(cls):
        session = DBSession()

        staffCount = session.query(StaffManage).count()
        customerCount = session.query(CustomerManage).count()
        supplierCount = session.query(Supplier).count()
        gasCount = session.query(GasManage).count()
        tractorCount = session.query(TractorManage).count()
        trailerCount = session.query(TrailerManage).count()
        session.close()

        return {"staffCount": staffCount,
                "customerCount": customerCount,
                "supplierCount": supplierCount,
                "gasCount": gasCount,
                "tractorCount": tractorCount,
                "trailerCount": trailerCount
                }

    # 计算当前日期与指定日期的间隔天数(日期字串分隔符"-")
    @classmethod
    def getIntervalDays(cls, dateTarget):
        dateStr = dateTarget.split("-")
        target = datetime.date(int(dateStr[0]), int(dateStr[1]), int(dateStr[2]))
        today = datetime.date.today()
        days = rrule.rrule(rrule.DAILY, dtstart=today, until=target).count()
        return days

    # 计算指定间隔月份的日期
    @classmethod
    def getIntervalMonthDate(cls, startDate, intervalMonth):
        dateStr = startDate.split("-")
        currentDate = datetime.date(int(dateStr[0]), int(dateStr[1]), int(dateStr[2]))
        return currentDate + relativedelta(months=intervalMonth)

    # 筛选条件：上次年检时间 + 年检周期 - 当前日期 <= 15 天
    @classmethod
    def getMaintenanceTipsForHome(cls):
        session = DBSession()
        allTips = []
        queryAllTractor = session.query(TractorManage).all()
        for item in queryAllTractor:
            # 上次年检时间
            lastAnnualInspectionTime = item.annualInspectionTime.strftime("%Y-%m-%d")
            # 年检周期
            cycle = item.annualInspectionCycle
            # 下次年检日期
            dateNext = BaseViewUtils.getIntervalMonthDate(lastAnnualInspectionTime, cycle).strftime("%Y-%m-%d")
            intervalDays = BaseViewUtils.getIntervalDays(dateNext)
            if intervalDays <= 30:
                tipItem = VehicleMaintenanceTip("拖车", item.tractorID, lastAnnualInspectionTime, cycle, dateNext,
                                                intervalDays)
                tip_json = json.dumps(object2dict(tipItem), cls=DateEncoder)
                tip = json.loads(tip_json)
                allTips.append(tip)

        queryAllTailer = session.query(TrailerManage).all()
        for item in queryAllTailer:
            lastAnnualInspectionTime = item.annualInspectionTime.strftime("%Y-%m-%d")
            cycle = item.annualInspectionCycle
            dateNext = BaseViewUtils.getIntervalMonthDate(lastAnnualInspectionTime, cycle).strftime("%Y-%m-%d")
            intervalDays = BaseViewUtils.getIntervalDays(dateNext)
            if intervalDays <= 30:
                tipItem = VehicleMaintenanceTip("挂车", item.trailerID, lastAnnualInspectionTime, cycle, dateNext,
                                                intervalDays)
                tip_json = json.dumps(object2dict(tipItem), cls=DateEncoder)
                tip = json.loads(tip_json)
                allTips.append(tip)

        session.close()
        return allTips
